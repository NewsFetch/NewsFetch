import argparse
import json
import logging
import time

import config
import utils
from opensearch_client import OpenSearchClient

logging.basicConfig(level=logging.INFO)


class OpenSearchIndexer():
    def __init__(self, index_name: str):
        self.opensearch_client = OpenSearchClient(index_name=index_name)

    def create_index(self):
        create_index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }
        self.opensearch_client.create_index(create_index_body=create_index_body)

    def index(self, in_file: str):
        with open(in_file) as f:
            data = json.load(f)
            result = self.opensearch_client.index(body=data,
                                         id=data["id"],
                                         refresh=True)
        return result


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--enrichments-base-dir', type=str,
                        default="../../sample-data/CC-NEWS-20220918140302-00985/enrichments",
                        required=False,
                        help='full path to NewsFetch processed content root')
    args = parser.parse_args()

    if not args.enrichments_base_dir:
        logging.error("enrichments_base_dir is required!")
        print(parser.print_help())
        exit(1)

    file_names = utils.list_files(
        root_dir=args.enrichments_base_dir,
        pattern="**/*.json"
    )

    opensearch_indexer = OpenSearchIndexer(config.INDEX_NAME)
    opensearch_indexer.opensearch_client.delete_index()
    opensearch_indexer.create_index()

    for file_name in file_names:
        try:
            logging.info(f"indexing enrichments from {file_name}...")
            opensearch_indexer.index(file_name)
        except Exception as e:
            logging.error(f"error indexing enrichments from file: {file_name} due to: {e}")

    metrics = {
        "took": (time.time() - start_time),
        "num_processed": len(file_names)
    }
    logging.info(metrics)

    logging.info(opensearch_indexer.opensearch_client.search_with_searcher({"query": {"match_all": {}}}))

    exit(0)
