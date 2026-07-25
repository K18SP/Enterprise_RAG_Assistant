from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    """
    User query sent to the RAG system.
    """

    query: str = Field(
        min_length=1,
        description="Question to ask the RAG system."
    )   
    retrieve_k: int = Field(
        default=5,
        description = 'Number of documents to retrieve initially.'
    )
    rerank_k: int = Field(
        default=3,
        description = 'Number of top documents to keep after reranking' 
    )
