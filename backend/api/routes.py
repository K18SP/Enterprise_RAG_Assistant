from fastapi import APIRouter, Depends
from schemas.rag_request import RAGRequest
from schemas.rag_response import RAGResponse
from services.rag_service import RAGService
from api.dependencies import get_rag_service

router = APIRouter(
    prefix='/rag',
    tags=['RAG']
)

@router.post("/ask", response_model=RAGResponse)
def ask_question(
    request: RAGRequest, 
    rag_service: RAGService = Depends(get_rag_service)
) -> RAGResponse:
    # Pass the new fields from the request body into the service layer
    return rag_service.ask(
        query=request.query,
        retrieve_k=request.retrieve_k,
        rerank_k=request.rerank_k
    )

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/version")
def version():
    return {"version": "1.0.0"}
