from .base_retriever import BaseRetriever

from vectordb.vectorstore_factory import VectorStoreFactory

class SimilarityRetriever(BaseRetriever):

    """
    -> Find and return the text chunks whose vector embeddings are mathematically closest to your search query using metrics like cosine similarity or Euclidean distance.
    -> Ranks every document by its direct score to the query and outputs the top K results.
    -> Best used for narrow, factual queries and exact lookups
    """

    def __init__(self,vector_db):

        self.vector_db = vector_db

    def retrieve(self, query: str, k: int = 5):
        return self.vector_db.similarity_search(query,k)