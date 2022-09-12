import logging
import os
import pathlib

import time
import boto3
import config

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

COMMOM_CRAWL_BUCKET = 'commoncrawl'
COMMOM_CRAWL_CC_NEWS_PREFIX = 'crawl-data/CC-NEWS/'

class GetLatestNewsWarcArchive():
    def fetch_most_recent_file(self, common_crawl_data_dir: str) -> tuple[str, str]:
        logging.info("fetching most recent warc file from common crawl...")
        logging.info("destination folder is %s", common_crawl_data_dir)

        get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
        s3_client = boto3.client('s3')

        most_recent_file = None
        paginator = s3_client.get_paginator("list_objects")
        page_iterator = paginator.paginate(Bucket=COMMOM_CRAWL_BUCKET, Prefix=COMMOM_CRAWL_CC_NEWS_PREFIX)
        for page in page_iterator:
            if "Contents" in page:
                # most recent file can be warc.paths.gz. so fetching the second to last file
                most_recent_file = [obj['Key'] for obj in sorted(page["Contents"], key=get_last_modified)][-2]
        warc_file_name = most_recent_file.split("/")[-1]
        logging.info("most recent warc file is %s", warc_file_name)

        destination_file = os.path.join(common_crawl_data_dir, warc_file_name)
        pathlib.Path(destination_file).parent.mkdir(parents=True, exist_ok=True)
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(COMMOM_CRAWL_BUCKET)
        bucket.download_file(most_recent_file, destination_file)
        logging.info("downloaded most recent warc file to %s", destination_file)

        return warc_file_name, destination_file

def main():
    start_time = time.time()
    warc_file_name, destination_file = GetLatestNewsWarcArchive().fetch_most_recent_file(config.COMMON_CRAWL_DATA_DIR)
    loginfo = {
        "warc_file_name": warc_file_name,
        "destination_file": destination_file,
        "took": (time.time() - start_time),
    }
    logging.info(loginfo)


if __name__ == '__main__':
    main()