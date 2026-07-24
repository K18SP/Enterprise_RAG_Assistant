from typing import Any

from pydantic import BaseModel, Field

from .retrieved_document import RetrievedDocument

from schemas.rag_metadata import RAGMetadata


class RAGResponse(BaseModel):
    """
    Response returned by the RAG pipeline.
    """

    query: str

    answer: str

    context: str

    documents: list[RetrievedDocument]

    metadata: RAGMetadata