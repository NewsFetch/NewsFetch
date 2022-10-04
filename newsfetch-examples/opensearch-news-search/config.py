import os

from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME", "newsfetch")
OPENSEARCH_HOST = os.environ.get("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = os.environ.get("OPENSEARCH_PORT", 9200)