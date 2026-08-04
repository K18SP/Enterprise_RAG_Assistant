from pydantic import BaseModel


class UploadResponse(BaseModel):

    document_id: str

    filename: str
    extension: str
    size_bytes: int

    documents_loaded: int
    chunks_created: int

    status: str