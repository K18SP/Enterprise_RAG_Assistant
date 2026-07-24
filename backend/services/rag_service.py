from pipeline.pipeline_factory import PipelineFactory
from schemas.rag_response import RAGResponse

from utils.logger import setup_logger
from exceptions.pipeline_exception import PipelineError

logger = setup_logger(__name__)


class RAGService:
    """
    Service layer responsible for interacting with the RAG pipeline.

    This class acts as the bridge between the API layer and the
    underlying RAG pipeline.
    """

    def __init__(self):
        logger.info("Initializing RAG Service.")

        self.pipeline = PipelineFactory.create_pipeline()

        logger.info("RAG Service initialized successfully.")

    def ask(self, query: str) -> RAGResponse:
        """
        Process a user query using the RAG pipeline.

        Args:
            query: User question.

        Returns:
            RAGResponse containing the answer and supporting documents.
        """

        logger.info(f"Received query: {query}")

        try:
            response = self.pipeline.ask(query)

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