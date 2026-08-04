from pipeline.pipeline_factory import PipelineFactory
from schemas.rag_response import RAGResponse
from utils.logger import setup_logger
from exceptions.pipeline_exception import PipelineError

logger = setup_logger(__name__)

class RAGService:
    """
    Service layer responsible for interacting with the RAG pipeline.
    This class acts as the bridge between the API layer and the underlying RAG pipeline.
    """
    def __init__(self,vector_db = None):
        logger.info("Initializing RAG Service.")
        self.pipeline = PipelineFactory.create_pipeline(vector_db=vector_db)
        logger.info("RAG Service initialized successfully.")

    def ask(self, query: str, retrieve_k: int, rerank_k: int) -> RAGResponse:
        """
        Process a user query using the RAG pipeline.

        Args:
            query: User question.
            retrieve_k: Number of relevant documents to retrieve.
            rerank_k: Number of top documents to keep after reranking.

        Returns:
            RAGResponse containing the answer and supporting documents.
        """
        # Business logic validation: Ensure rerank limit doesn't exceed retrieval limit
        if rerank_k > retrieve_k:
            logger.warning(f"rerank_k ({rerank_k}) is greater than retrieve_k ({retrieve_k}). Capsulated rerank_k to retrieve_k.")
            rerank_k = retrieve_k

        logger.info(f"Received query: '{query}' | retrieve_k: {retrieve_k} | rerank_k: {rerank_k}")
        
        try:
            # Forward the parameters down to your pipeline architecture
            response = self.pipeline.ask(
                query=query, 
                retrieve_k=retrieve_k, 
                rerank_k=rerank_k
            )
            logger.info("Query processed successfully.")
            return response
        except PipelineError:
            logger.exception("Pipeline execution failed.")
            raise
        except Exception as e:
            logger.exception("Unexpected error while processing query.")
            raise PipelineError(
                "An unexpected error occurred while processing the query."
            ) from e
