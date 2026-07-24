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

        #Step 1
        documents = self.retriever.retrieve(query = query, k=retrieve_k)

        #Step 2
        documents = self.reranker.rerank(query = query, documents = documents, top_k = rerank_k)

        response_documents = DocumentMapper.to_response_list(documents)

        #Step 3
        context = ContextBuilder.build_context(documents)

        #Step 4
        answer = self.llm.generate(query=query, context = context)

        return RAGResponse(
            query=query,
            answer=answer,
            context=context,
            documents=response_documents,
            metadata={
                "retrieved_documents": retrieve_k,
                "reranked_documents": rerank_k
            }
        )