from pathlib import Path
from openai import OpenAI


def load_api_key():
    with open("secret.txt","r",encoding="utf-8") as f:
        return f.read().strip()


API_KEY = load_api_key()

BASE_URL = "https://api2.gptsapi.net/v1"
CHAT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-large"

CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
TOP_K = 5
MAX_CONTEXT_CHARS = 1500


def get_client():
    return OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )


ROOT_DIR = Path(__file__).resolve().parent
DOCS_DIR = ROOT_DIR.parent / "docs"
DATA_DIR = ROOT_DIR / "data"
SOURCE_DIR = DATA_DIR / "source"
CHUNK_DIR = DATA_DIR / "chunks"
CHUNK_FILE = CHUNK_DIR / "chunks.json"
VECTOR_DB_DIR = ROOT_DIR / "vector_db"
