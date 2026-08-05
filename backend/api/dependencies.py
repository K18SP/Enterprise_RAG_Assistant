from fastapi import Request

from services.rag_service import RAGService
from services.document_service import DocumentService

from fastapi import Header

from services.user_workspace import UserWorkspace

from fastapi import Depends

from sqlalchemy.orm import Session

from database.database import get_db

from auth.auth_service import AuthService


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

def get_auth_service(

    db: Session = Depends(
        get_db
    )

) -> AuthService:

    return AuthService(
        db
    )