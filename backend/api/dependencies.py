from fastapi import Request

from services.rag_service import RAGService


def get_rag_service(
    request: Request
) -> RAGService:
    """
    Return the singleton RAG service stored in FastAPI state.
    """

    return request.app.state.rag_service