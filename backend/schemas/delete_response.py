from pydantic import BaseModel


class DeleteResponse(BaseModel):

    document_id: str

    filename: str

    chunks_deleted: int

    status: str