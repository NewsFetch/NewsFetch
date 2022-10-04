import argparse
import json
import logging
import os
import time
from glob import glob
import config

from opensearch_client import OpenSearchClient

def list_files(root_dir: str, pattern: str):
    path_pattern = os.path.join(root_dir, pattern)
    print(path_pattern)
    files = glob(path_pattern, recursive=True)
    return files

class OpenSearchIndexer():
    def __init__(self, index_name: str):
        self.opensearch_client = OpenSearchClient(index_name=index_name)

    def index(self, in_file: str):
        with open(in_file) as f:
            data = json.load(f)
            self.opensearch_client.save_enrichment(data)
        return in_file


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--enrichments-base-dir', type=str, required=True, help='full path to NewsFetch processed content root')
    args = parser.parse_args()

    if not args.enrichments_base_dir:
        logging.error("enrichments_base_dir is required!")
        print(parser.print_help())
        exit(1)

    file_names = list_files(
        root_dir=args.enrichments_base_dir,
        pattern="**/*.json"
    )

    opensearch_indexer = OpenSearchIndexer(config.INDEX_NAME)

    for file_name in file_names:
        try:
            logging.info(f"index enrichments from {file_name}...")
            opensearch_indexer.index(file_name)
        except Exception as e:
            logging.error(f"error indexing enrichments from file: {file_name} due to: {e}")


    metrics = {
        "took": (time.time() - start_time),
        "num_processed": len(file_names)
    }
    print(metrics)
    exit(0)
