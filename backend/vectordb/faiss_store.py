from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from .base_vectorstore import BaseVectorStore

from utils.logger import setup_logger

logger = setup_logger(__name__)

from exceptions.vectorstore_exception import VectorStoreError

from config.constants import VECTOR_DB_SAVE_PATH

class FAISSStore(BaseVectorStore):

    def __init__(self,embedding,save_path:str):

        self.embedding = embedding

        self.db = None

        self.save_path = VECTOR_DB_SAVE_PATH

        logger.info(f"Initializing FAISS vector store at '{self.save_path}'.")

    def add_documents(self, documents:List[Document]):

        logger.info(f"Adding {len(documents)} document(s) to the vector store.")

        try:

            self.db = FAISS.from_documents(documents,self.embedding.embedding)

            logger.info("Documents indexed successfully.")

        except Exception as e:

            logger.exception("Failed to create FAISS index.")

            raise VectorStoreError("Failed to create FAISS index.") from e
        

    def similarity_search(self, query, k=5):

        if self.db is None:
            raise VectorStoreError(
            "Vector database is not loaded."
        )

        try:

            return self.db.similarity_search(query, k=k)

        except Exception as e:

            logger.exception("Similarity search failed.")

            raise VectorStoreError("Failed to perform similarity search.") from e

    def mmr_search(self, query, k=5, fetch_k=20):

        try:

            return self.db.max_marginal_relevance_search(query, k=k, fetch_k = fetch_k)

        except Exception as e:

            logger.exception("Relevant search failed")

            raise VectorStoreError("Relevant search failed") from e
    
    def save(self):

        logger.info(f'Saving FAISS index to {self.save_path}')

        if self.db is None:
            raise ValueError(
                "No vector database to save. Call add_documents() first."
            )

        try:

            Path(self.save_path).mkdir(parents=True, exist_ok=True)

            self.db.save_local(self.save_path)

        except Exception as e:

            logger.exception("Failed to save FAISS index.")
            raise VectorStoreError("Failed to save vector database") from e
        
    def load(self):

        logger.info(f"Loading FAISS index from '{self.save_path}'.")

        try:

            self.db = FAISS.load_local(self.save_path, self.embedding.embedding, allow_dangerous_deserialization=True)
            logger.info("FAISS index loaded succesfully")

        except Exception as e:

            logger.exception("Failed to load FAISS index.")
            raise VectorStoreError("Failed to load vector database") from e