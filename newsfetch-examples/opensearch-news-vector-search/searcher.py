import logging

from sentence_transformers import SentenceTransformer

import config
from opensearch_client import OpenSearchClient

MODEL = SentenceTransformer('all-MiniLM-L6-v2')

logging.basicConfig(level=logging.INFO)


class OpenSearchVectorSearcher():
    def __init__(self, index_name: str):
        self.opensearch_client = OpenSearchClient(index_name=index_name)

    def search_with_query_vector(self, query):
        embeddings = MODEL.encode([query])
        query = {
            "size": 2,
            "query": {
                "knn": {
                    "content_vector": {
                        "vector": embeddings[0],
                        "k": 2
                    }
                }
            }
        }

        response = self.opensearch_client.search_with_searcher(searcher=query)

        logging.info('Search results:')
        for hit in response["hits"]["hits"]:
            logging.info(hit["_source"]["content"])

if __name__ == "__main__":
    searcher = OpenSearchVectorSearcher(index_name=config.VECTOR_INDEX_NAME)
    searcher.search_with_query_vector('how to help migrants')