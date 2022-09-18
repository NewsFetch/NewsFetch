import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MAX_LIMIT = 25
DATABASE_URL = os.environ.get("DATABASE_URL")
MAX_LIMIT = int(os.environ.get("MAX_LIMIT", DEFAULT_MAX_LIMIT))
PARSE_ENABLED = os.environ.get("PARSE_ENABLED", "false").lower() == "false"