from pydantic import BaseModel

from .retrieved_document import RetrievedDocument


class RAGResponse(BaseModel):

    query: str

    answer: str

    context: str

    documents: list[RetrievedDocument]

    metadata: dict