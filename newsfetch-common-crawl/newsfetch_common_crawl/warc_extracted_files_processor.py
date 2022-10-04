import argparse
import concurrent.futures
import json
import logging
import os
import datetime
import time

from newsfetch_core.common import util
from newsfetch_newsplease.newplease_adapter import NewsPleaseHtmlAdapter
import config

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

# add list of sites to skip
stop_sites = []

def process_warc_content_dir(root_dir):
    num_processed = 0
    warc_extract_dir = os.path.join(root_dir, config.WARC_EXTRACT_DIR)

    try:
        logging.debug(f'processing warc content dir: {warc_extract_dir}...')
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for root, dirs, files in os.walk(warc_extract_dir):
                for file_name in files:
                    full_path = os.path.join(root, file_name)
                    if full_path.endswith(config.JSON_OUT_FILE_EXT):
                        logging.debug(f'processing file: {full_path}...')
                        num_processed = num_processed + 1
                        content_processor_wrapper = ContentProcessorWrapper(file_name=full_path, root_dir=root_dir)
                        futures.append(executor.submit(content_processor_wrapper.process_warc_content))

        for future in concurrent.futures.as_completed(futures):
            future.result()


    except Exception as e:
        print(f'exception occurred processing warc content dir: {warc_extract_dir} -> {e}')

    return num_processed


class ContentProcessorWrapper():
    def __init__(self, file_name, root_dir):
        self.file_name = file_name
        self.root_dir = root_dir

    def process_warc_content(self):
        try:
            with(open(self.file_name, "r+")) as warc_extract_file:
                warc_extract = json.loads(warc_extract_file.read())
                uri = warc_extract["uri"]
                logging.debug(f'extracting content for: {uri}...')

                domain = warc_extract["domain"]
                dataset_id = warc_extract["dataset_id"]
                article_html = warc_extract["article_html"]

                if domain in stop_sites:
                    logging.warning(f'WARNING: did not extract content for: {uri}... domain in stop list')
                    return

                article = NewsPleaseHtmlAdapter(article_html, uri).get_article()

                meta_info = {
                    "dataset_id": dataset_id,
                    "dataset": warc_extract["dataset"],
                    "dataset_content_length": warc_extract["dataset_content_length"],
                    "warc_sourced_date": warc_extract["warc_sourced_date"],
                    "warc_extracted_date": warc_extract["warc_extracted_date"],
                    "warc_processed_date": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                }

                article_json = article.dict()
                if article_json["published_date"]:
                    article_json["published_date"] = article_json["published_date"].strftime('%Y-%m-%dT%H:%M:%SZ')

                article_json["meta_info"] = meta_info

                file_name = dataset_id + config.JSON_OUT_FILE_EXT
                util.write_json_to_file([self.root_dir, config.PROCESSED_CONTENT_DIR, domain], file_name, data=article_json)

        except Exception as e:
            print(f'exception occurred processing warc file: {file_name} -> {e}')


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--warc-file-path', type=str, required=True, help='full path to compressed warc file')
    args = parser.parse_args()

    if not args.warc_file_path:
        logging.error("warc-file-path is required!")
        print(parser.print_help())
        exit(1)

    file_path = os.path.join(args.warc_file_path)
    root_directory = util.get_warc_file_name(file_path)
    logging.info(f'processing warc file: {file_path}...')
    logging.info(f'root_directory is: {root_directory}...')
    num_processed = process_warc_content_dir(root_dir=root_directory)

    metrics = {
        "took": (time.time() - start_time),
        "num_processed": num_processed
    }
    print(metrics)
    exit(0)
