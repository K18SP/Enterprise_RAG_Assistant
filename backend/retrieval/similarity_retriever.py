from .base_retriever import BaseRetriever

from vectordb.vectorstore_factory import VectorStoreFactory

class SimilarityRetriever(BaseRetriever):

    def __init__(self,vector_db):

        self.vector_db = vector_db

    def retrieve(self, query: str, k: int = 5):
        return self.vector_db.similarity_search(query,k)