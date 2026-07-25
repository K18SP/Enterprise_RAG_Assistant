from .base_retriever import BaseRetriever

from vectordb.vectorstore_factory import VectorStoreFactory

class MMRRetriever(BaseRetriever):

    """
    -> Maximum Marginal Relevance
    -> Operates iteratively. It fetches a larger initial pool of documents (fetch k), picks the most relevant item first, and then penalizes subsequent candidates that are too similar to items already chosen.
    -> Balance relevance to the query with diversity among the retrieved documents to eliminate redundancy.
    -> Best used for Broad exploratory searches and complex research topics.
    """

    def __init__(self,vector_db):

        self.vector_db = vector_db

    def retrieve(self, query: str, k: int = 5):
        return self.vector_db.mmr_search(query,k=k,fetch_k=20)
