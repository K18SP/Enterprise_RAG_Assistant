from pydantic import BaseModel


class DocumentRecord(BaseModel):

    document_id: str

    filename: str
    stored_filename: str

    extension: str
    size_bytes: int

    documents_loaded: int
    chunks_created: int