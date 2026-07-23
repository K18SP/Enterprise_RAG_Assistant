from .base_retriever import BaseRetriever

from vectordb.vectorstore_factory import VectorStoreFactory

class MMRRetriever(BaseRetriever):

    def __init__(self,vector_db):

        self.vector_db = vector_db

    def retrieve(self, query: str, k: int = 5):
        return self.vector_db.mmr_search(query,k=k,fetch_k=20)
