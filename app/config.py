import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
TOP_K = int(os.getenv("TOP_K", "5"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
KNOWLEDGE_DIR = "data/knowledge"
VECTOR_DIR = "data/vector_store"
