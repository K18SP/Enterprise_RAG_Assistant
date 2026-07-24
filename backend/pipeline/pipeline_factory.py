from embeddings.embedding_factory import EmbeddingFactory
from vectordb.vectorstore_factory import VectorStoreFactory
from retrieval.retriever_factory import RetrieverFactory
from reranker.reranker_factory import RerankerFactory
from llm.llm_factory import LLMFactory

from .rag_pipeline import RAGPipeline

from config.constants import (
    EMBEDDING_PROVIDER,
    VECTORSTORE,
    RETRIEVER,
    RERANKER,
    LLM_PROVIDER
)   

class PipelineFactory:

    @staticmethod
    def create_pipeline():

        #Create embedding model
        embedding = EmbeddingFactory.get_embedding(provider=EMBEDDING_PROVIDER)

        #Create vector database
        vector_db = VectorStoreFactory.get_vectorstore(embedding=embedding, vectorstore=VECTORSTORE)

        #Load existing FAISS index
        vector_db.load()

        #Create retriever
        retriever = RetrieverFactory.get_retriever(vector_db,RETRIEVER)

        #Create reranker
        reranker = RerankerFactory.get_reranker(RERANKER)

        #Create LLM
        llm = LLMFactory.get_llm(LLM_PROVIDER)

        #Build complete pipeline
        return RAGPipeline(retriever=retriever, reranker=reranker, llm=llm)