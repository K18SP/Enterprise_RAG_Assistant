from typing import List

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File
)

from services.document_service import DocumentService

from schemas.document_record import DocumentRecord
from schemas.upload_response import UploadResponse
from schemas.delete_response import DeleteResponse

from api.dependencies import get_document_service


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

@router.post(
    "/upload",
    response_model=UploadResponse
)
def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(
        get_document_service
    )
) -> UploadResponse:

    return document_service.process_document(
        file
    )


# =========================================================
# GET ALL DOCUMENTS
# =========================================================

@router.get(
    "",
    response_model=List[DocumentRecord]
)
def get_documents(
    document_service: DocumentService = Depends(
        get_document_service
    )
) -> List[DocumentRecord]:

    return document_service.get_documents()


# =========================================================
# GET DOCUMENT BY ID
# =========================================================

@router.get(
    "/{document_id}",
    response_model=DocumentRecord
)
def get_document(
    document_id: str,
    document_service: DocumentService = Depends(
        get_document_service
    )
) -> DocumentRecord:

    return document_service.get_document(
        document_id
    )


# =========================================================
# DELETE DOCUMENT
# =========================================================

@router.delete(
    "/{document_id}",
    response_model=DeleteResponse
)
def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(
        get_document_service
    )
) -> DeleteResponse:

    return document_service.delete_document(
        document_id
    )