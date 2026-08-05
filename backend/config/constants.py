from pathlib import Path

EMBEDDING_PROVIDER = "huggingface"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

VECTORSTORE = "faiss"

RETRIEVER = "similarity"

RERANKER = "cross_encoder"

LLM_PROVIDER = "groq"

LLM_MODEL = "llama-3.3-70b-versatile"

TEMPERATURE = 0.2

RETRIEVE_TOP_K = 10

RERANK_TOP_K = 5

VECTOR_DB_PATH = "models/faiss_index"

# VECTOR_DB_SAVE_PATH = 'data/vector_db'

# PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# DATA_DIR = PROJECT_ROOT / "data"



BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

VECTOR_DB_SAVE_PATH = DATA_DIR / "vector_db"

# UPLOAD_DIR = DATA_DIR / "uploads"

CHUNKING_STRATEGY = "recursive"

# DOCUMENT_REGISTRY_PATH = DATA_DIR / "document_registry.json"