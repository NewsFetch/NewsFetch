import json
import logging
import os
import datetime
import time

from newsfetch_core.common import constants, util

from newsfetch_core.newplease_adapter import NewsPleaseHtmlAdapter

with(open("STOP_SITES.txt", "r")) as stop_sites_file:
    stop_sites = stop_sites_file.read().split("\n")

def process_warc_content(file_name, input_dir):
    try:
        with(open(file_name, "r+")) as warc_extract_file:
            warc_extract = json.loads(warc_extract_file.read())
            uri = warc_extract["uri"]
            logging.debug(f'extracting content for: {uri}...')

            domain = warc_extract["domain"]
            dataset_id = warc_extract["dataset_id"]
            article_html = warc_extract["article_html"]

            if domain in stop_sites:
                logging.warning(f'WARNING: did not extract content for: {uri}... domain in stop list')
                return

            news = NewsPleaseHtmlAdapter(article_html, uri).get_news()

            metadata = {
                "dataset_id": dataset_id,
                "dataset": warc_extract["dataset"],
                "dataset_content_length": warc_extract["dataset_content_length"],
                "warc_sourced_date": warc_extract["warc_sourced_date"],
                "warc_extracted_date": warc_extract["warc_extracted_date"],
                "warc_processed_date": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            }

            news["metadata"] = metadata

            file_name = dataset_id + constants.JSON_OUT_FILE_EXT
            util.write_json_to_file([input_dir, constants.PROCESSED_CONTENT_DIR, domain], file_name, data=news)

    except Exception as e:
        print(f'exception occurred processing warc file: {file_name} -> {e}')


if __name__ == '__main__':
    start_time = time.time()
    input_warc_filename = 'CC-NEWS-20220903010650-00655.warc.gz'
    file_path = os.path.join(input_warc_filename)
    input_directory = util.get_warc_file_name(file_path)

    dir_name = os.path.join(input_directory, constants.WARC_EXTRACT_DIR)
    file_names = util.list_files(dir_name, limit=False, limit_value=1000)

    # single threaded - todo: parallelize
    for file_name in file_names:
        process_warc_content(file_name, input_directory)

    metrics = {
        "took": (time.time() - start_time),
        "num_processed": len(file_names)
    }
    print(metrics)
