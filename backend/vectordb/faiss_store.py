from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from .base_vectorstore import BaseVectorStore
from embeddings.embedding_factory import EmbeddingFactory

class FAISSStore(BaseVectorStore):

    def __init__(self,embedding):

        self.embedding = embedding

        self.db = None

        self.save_path = 'data/vector_db'

    def add_documents(self, documents:List[Document]):

        self.db = FAISS.from_documents(documents, self.embedding.embedding)

    def similarity_search(self, query, k=5):

        if self.db is None:
            raise ValueError(
            "Vector database is not loaded."
        )

        return self.db.similarity_search(query, k=k)

    def mmr_search(self, query, k=5, fetch_k=20):

        return self.db.max_marginal_relevance_search(query, k=k, fetch_k = fetch_k)
    
    def save(self):

        if self.db is None:
            raise ValueError(
                "No vector database to save. Call add_documents() first."
            )

        Path(self.save_path).mkdir(parents=True, exist_ok=True)

        self.db.save_local(self.save_path)

    def load(self):

        self.db = FAISS.load_local(self.save_path, self.embedding.embedding, allow_dangerous_deserialization=True)