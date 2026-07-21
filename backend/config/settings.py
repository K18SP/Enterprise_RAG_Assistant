from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

    COLLECTION_NAME = "enterprise_rag"

    QDRANT_HOST = "localhost"

    QDRANT_PORT = 6333


settings = Settings()