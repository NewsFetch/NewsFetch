import logging
import config
from opensearchpy import OpenSearch
AUTH = ('admin', 'admin')  # For testing only. Don't store credentials in code.

class OpenSearchClient():
    def __init__(self,
                 index_name: str = config.INDEX_NAME,
                 host: str = config.OPENSEARCH_HOST,
                 port: int = config.OPENSEARCH_PORT):
        self.index_name = index_name
        self.host = host
        self.port = port
        self.opensearch = None
        try:
            self.opensearch = OpenSearch(
                hosts=[{'host': host, 'port': port}],
                http_compress=True,
                http_auth=AUTH,
                # client_cert = client_cert_path,
                # client_key = client_key_path,
                use_ssl=True,
                verify_certs=False,
                ssl_assert_hostname=False,
                ssl_show_warn=False,
            )
            if self.opensearch.ping():
                logging.info('connected to OpenSearch!')
            else:
                logging.error('could not connect to OpenSearch!')
        except Exception as e:
            logging.error('count not connect to OpenSearch!', e)

    def delete_index(self):
        if self.opensearch.indices.exists(index=self.index_name):
            response = self.opensearch.indices.delete(self.index_name)
            logging.info('Deleting index...')
            logging.info(response)

    def create_index(self, create_index_body):
        try:
            if not self.opensearch.indices.exists(index=self.index_name):
                logging.info("Creating index...")
                return self.opensearch.indices.create(index=self.index_name, body=create_index_body)
        except Exception as ex:
            logging.error(str(ex))

    def index(self, body, id, refresh):
        return self.opensearch.index(index=self.index_name, body=body, id=id, refresh=refresh)

    def search_with_searcher(self, searcher):
        return self.opensearch.search(index=self.index_name, body=searcher)

    def get_by_id(self, id):
        return self.opensearch.get(index=self.index_name, id=id)["_source"]

    def get_by_uri(self, uri):
        searcher = {
            "query": {
                "term": {
                    "uri.keyword": uri,
                }
            },
        }
        return self.search_with_searcher(searcher=searcher)

