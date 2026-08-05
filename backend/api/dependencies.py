from fastapi import Request

from services.rag_service import RAGService
from services.document_service import DocumentService

from fastapi import Header

from services.user_workspace import UserWorkspace


def get_rag_service(
    request: Request
) -> RAGService:

    return request.app.state.rag_service


def get_document_service(
    request: Request
) -> DocumentService:

    return request.app.state.document_service

def get_workspace(

    x_user_id: str = Header(
        default="default",
        alias="X-User-Id"
    )

) -> UserWorkspace:

    return UserWorkspace(
        x_user_id
    )