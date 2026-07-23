from sentence_transformers import CrossEncoder
from langchain_core.documents import Document

from .base_reranker import BaseReranker

class CrossEncoderReranker(BaseReranker):

    def __init__(self):

        self.model = CrossEncoder("BAAI/bge-reranker-base")

    def rerank(self, query:str, documents: list[Document], top_k: int=5) -> list[Document]:

        if not documents:
            return []

        # Create (query, document) pairs
        pairs = [
            [query, doc.page_content]
            for doc in documents
        ]

        # Predict relevance scores
        scores = self.model.predict(pairs)

        # Combine documents with their scores
        doc_scores = list(zip(documents, scores))

        # Store reranker information inside metadata
        for doc, score in doc_scores:

            doc.metadata["reranker"] = {
                "model": "BAAI/bge-reranker-base",
                "score": float(score)
            }

        # Sort by score (highest first)
        doc_scores.sort(
            key=lambda item: item[1],
            reverse=True
        )

        # Return only the top-k documents
        reranked_docs = [
            doc
            for doc, score in doc_scores[:top_k]
        ]

        return reranked_docs