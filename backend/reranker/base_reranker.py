from abc import ABC, abstractmethod
from langchain_core.documents import Document

"""
-> Reranking means reevaluating retrieved candidates using a stronger relevance model and rearraging
them according to their relevance to the query.
->It uses two methods; Biencoder and Cross encoder
-> Biencoder creates embedding independetly 
-> Cross encoder examines query and document together
"""
class BaseReranker(ABC):

    @abstractmethod
    def rerank(self, query: str, documents: list[Document], top_k: int=5) -> list[Document]:
        """
        Rerank retrieved documents based on query relevance.
        """
        pass