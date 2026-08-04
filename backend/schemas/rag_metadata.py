from pydantic import BaseModel

from schemas.retrieval_metadata import RetrievalMetadata
from schemas.latency_metadata import LatencyMetadata


class RAGMetadata(BaseModel):

    retrieval: RetrievalMetadata

    reranking: RetrievalMetadata

    latency: LatencyMetadata