import os

from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME", "newsfetch")
VECTOR_INDEX_NAME = os.getenv("INDEX_NAME", "newsfetch-vector")
OPENSEARCH_HOST = os.environ.get("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = os.environ.get("OPENSEARCH_PORT", 9200)