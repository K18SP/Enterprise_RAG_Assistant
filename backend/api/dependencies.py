from fastapi import Request

from services.rag_service import RAGService
from services.document_service import DocumentService


def get_rag_service(
    request: Request
) -> RAGService:

    return request.app.state.rag_service


def get_document_service(
    request: Request
) -> DocumentService:

    return request.app.state.document_service