from pydantic import BaseModel


class LatencyMetadata(BaseModel):

    retrieval_ms: float

    reranking_ms: float

    context_ms: float

    llm_ms: float

    total_ms: float