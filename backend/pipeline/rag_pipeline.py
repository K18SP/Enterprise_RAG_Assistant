import time

from retrieval.base_retriever import BaseRetriever
from reranker.base_reranker import BaseReranker
from llm.base_llm import BaseLLM
from llm.context_builder import ContextBuilder

from schemas.rag_response import RAGResponse
from schemas.rag_metadata import RAGMetadata
from schemas.retrieval_metadata import RetrievalMetadata
from schemas.latency_metadata import LatencyMetadata

from mappers.document_mapper import DocumentMapper

from exceptions.pipeline_exception import PipelineError

from utils.logger import setup_logger


logger = setup_logger(__name__)


class RAGPipeline:

    def __init__(
        self,
        retriever: BaseRetriever,
        reranker: BaseReranker,
        llm: BaseLLM
    ):

        self.retriever = retriever
        self.reranker = reranker
        self.llm = llm

    def ask(
        self,
        query: str,
        retrieve_k: int = 10,
        rerank_k: int = 5
    ) -> RAGResponse:

        """
        Execute the complete RAG pipeline.

        Steps
        -----
        1. Retrieve documents
        2. Rerank documents
        3. Build context
        4. Generate answer
        5. Return structured response
        """

        logger.info(
            f"Processing query: {query}"
        )

        pipeline_start = time.perf_counter()

        retrieval_ms = 0.0
        reranking_ms = 0.0
        context_ms = 0.0
        llm_ms = 0.0

        try:

            # ---------------------------------------
            # STEP 1 : Retrieve Documents
            # ---------------------------------------

            retrieval_start = time.perf_counter()

            retrieved_documents = self.retriever.retrieve(
                query=query,
                k=retrieve_k
            )

            retrieval_ms = (
                time.perf_counter() - retrieval_start
            ) * 1000

            retrieved_count = len(
                retrieved_documents
            )

            logger.info(
                f"Retrieved {retrieved_count} document(s)."
            )

            # ---------------------------------------
            # STEP 2 : Rerank
            # ---------------------------------------

            rerank_start = time.perf_counter()

            reranked_documents = self.reranker.rerank(
                query=query,
                documents=retrieved_documents,
                top_k=rerank_k
            )

            reranking_ms = (
                time.perf_counter() - rerank_start
            ) * 1000

            reranked_count = len(
                reranked_documents
            )

            logger.info(
                f"Reranked to {reranked_count} document(s)."
            )

            # ---------------------------------------
            # STEP 3 : Build Context
            # ---------------------------------------

            context_start = time.perf_counter()

            context = ContextBuilder.build_context(
                reranked_documents
            )

            context_ms = (
                time.perf_counter() - context_start
            ) * 1000

            # ---------------------------------------
            # STEP 4 : Generate Answer
            # ---------------------------------------

            logger.info(
                "Generating response using LLM."
            )

            llm_start = time.perf_counter()

            answer = self.llm.generate(
                query=query,
                context=context
            )

            llm_ms = (
                time.perf_counter() - llm_start
            ) * 1000

            logger.info(
                "LLM response generated successfully."
            )

            # ---------------------------------------
            # STEP 5 : Convert Documents
            # ---------------------------------------

            response_documents = (
                DocumentMapper.to_schema_list(
                    reranked_documents
                )
            )

            # ---------------------------------------
            # Total Pipeline Time
            # ---------------------------------------

            total_ms = (
                time.perf_counter() - pipeline_start
            ) * 1000

            # ---------------------------------------
            # Return Response
            # ---------------------------------------

            return RAGResponse(

                query=query,

                answer=answer,

                context=context,

                documents=response_documents,

                metadata=RAGMetadata(

                    retrieval=RetrievalMetadata(

                        requested=retrieve_k,

                        returned=retrieved_count

                    ),

                    reranking=RetrievalMetadata(

                        requested=rerank_k,

                        returned=reranked_count

                    ),

                    latency=LatencyMetadata(

                        retrieval_ms=round(
                            retrieval_ms,
                            2
                        ),

                        reranking_ms=round(
                            reranking_ms,
                            2
                        ),

                        llm_ms=round(
                            llm_ms,
                            2
                        ),

                        total_ms=round(
                            total_ms,
                            2
                        )

                    )

                )

            )

        except Exception as e:

            logger.exception(
                "Pipeline execution failed."
            )

            raise PipelineError(
                "Failed to process query."
            ) from e

        finally:

            total_ms = (
                time.perf_counter() - pipeline_start
            ) * 1000

            logger.info(

                f"Latency | "

                f"Retrieval: {retrieval_ms:.2f} ms | "

                f"Reranking: {reranking_ms:.2f} ms | "

                f"Context: {context_ms:.2f} ms | "

                f"LLM: {llm_ms:.2f} ms | "

                f"Total: {total_ms:.2f} ms"

            )