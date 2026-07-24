from retrieval.base_retriever import BaseRetriever
from reranker.base_reranker import BaseReranker
from llm.base_llm import BaseLLM
from llm.context_builder import ContextBuilder
from schemas.rag_response import RAGResponse
from mappers.document_mapper import DocumentMapper

class RAGPipeline:

    def __init__(self, retriever: BaseRetriever, reranker: BaseReranker, llm: BaseLLM):

        self.retriever = retriever
        self.reranker = reranker
        self.llm = llm

    def ask(self, query:str, retrieve_k: int=10, rerank_k: int=5) -> RAGResponse:
        """
        Execute the complete RAG pipeline.

        Steps:
        1. Retrieve relevant documents
        2. Rerank retrieved documents
        3. Build LLM context
        4. Generate answer
        5. Return structured response
        """

        #Step 1 - Retrieve relevant documents
        retrieved_documents = self.retriever.retrieve(query = query, k=retrieve_k)

        retrieved_cnt = len(retrieved_documents)

        #Step 2 - Rerank retrieved documents
        reranked_documents = self.reranker.rerank(query = query, documents = retrieved_documents, top_k = rerank_k)

        reranked_cnt = len(reranked_documents)

        # Convert internal documents to response schemas
        response_documents = DocumentMapper.to_schema_list(reranked_documents)

        #Step 3 - Build context for the LLM
        context = ContextBuilder.build_context(reranked_documents)

        #Step 4 - Generate final answer
        answer = self.llm.generate(query=query, context = context)

        return RAGResponse(
            query=query,
            answer=answer,
            context=context,
            documents=response_documents,
            metadata={
                "retrieval": {
                    "requested": retrieve_k,
                    "returned": retrieved_cnt
                },
                "reranking": {
                    "requested": rerank_k,
                    "returned": reranked_cnt
                }
            }
        )