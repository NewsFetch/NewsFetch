import logging

import config
from opensearchpy import OpenSearch


class OpenSearchClient():
    def __init__(self,
                 index_name: str = config.INDEX_NAME,
                 host: str = config.OPENSEARCH_HOST,
                 port: int = config.OPENSEARCH_PORT):
        self.index_name = index_name
        self.host = host
        self.port = port
        self.opensearch_client = None
        try:
            self.opensearch_client = OpenSearch([{'host': self.host, 'port': self.port}])
            if self.opensearch_client.ping():
                logging.info('connected to OpenSearch!')
            else:
                logging.error('could not connect to OpenSearch!')
        except Exception as e:
            logging.error('count not connect to OpenSearch!', e)

    def create_index(self):
        # index settings
        create_index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }
        try:
            if not self.opensearch_client.indices.exists(index=self.index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                return self.opensearch_client.indices.create(index=self.index_name, body=create_index_body)
        except Exception as ex:
            print(str(ex))

    def search_with_searcher(self, searcher):
        return self.opensearch_client.search(index=self.index_name, body=searcher)

    def save_enrichment(self, data):
        try:
            result = self.opensearch_client.index(index=self.index_name,
                                                  body=data,
                                                  id=data["id"],
                                                  refresh=True)
            return result
        except Exception as ex:
            logging.error('Error in indexing data')
            logging.error(str(ex))

    def get_enrichment_by_id(self, id):
        return self.opensearch_client.get(index=self.index_name, id=id)["_source"]

    def get_enrichments_by_uri(self, uri):
        searcher = {
            "query": {
                "term": {
                    "uri.keyword": uri,
                }
            },
        }
        return self.search_with_searcher(searcher=searcher)

if __name__ == "__main__":
    opensearch_client = OpenSearchClient()
    opensearch_client.create_index()
    print(opensearch_client.search_with_searcher({"query": {"match_all": {}}}))