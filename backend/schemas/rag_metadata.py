from schemas.retrieval_metadata import RetrievalMetadata
from pydantic import BaseModel

class RAGMetadata(BaseModel):
    retrieval: RetrievalMetadata
    reranking: RetrievalMetadata