import logging
import time

import boto3

class GetLatestNewsWarcArchive():
    def fetch_most_recent_file(self):
        get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
        s3_client = boto3.client('s3')

        most_recent_file = None
        paginator = s3_client.get_paginator("list_objects")
        page_iterator = paginator.paginate(Bucket="commoncrawl", Prefix="crawl-data/CC-NEWS/")
        for page in page_iterator:
            if "Contents" in page:
                # most recent file can be warc.paths.gz. so fetching the second to last file
                most_recent_file = [obj['Key'] for obj in sorted(page["Contents"], key=get_last_modified)][-2]
        warc_file_name = most_recent_file.split("/")[-1]

        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket("commoncrawl")
        bucket.download_file(most_recent_file, warc_file_name)

if __name__ == '__main__':
    start_time = time.time()
    GetLatestNewsWarcArchive().fetch_most_recent_file()
    metrics = {
        "took": (time.time() - start_time),
    }
    logging.info(metrics)
