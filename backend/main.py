from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import router as rag_router
from api.document_routes import router as document_router
from api.exception_handlers import register_exception_handlers

from vectordb.vectorstore_factory import VectorStoreFactory
from embeddings.embedding_factory import EmbeddingFactory

from services.rag_service import RAGService
from services.document_service import DocumentService
from services.document_registry import DocumentRegistry

from config.constants import (
    EMBEDDING_PROVIDER,
    VECTORSTORE,
    DOCUMENT_REGISTRY_PATH
)

from utils.logger import setup_logger


logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting Enterprise RAG API...")

    # ---------------------------------------
    # STEP 1: Create shared embedding model
    # ---------------------------------------

    embedding = EmbeddingFactory.get_embedding(
        EMBEDDING_PROVIDER
    )

    # ---------------------------------------
    # STEP 2: Create shared vector store
    # ---------------------------------------

    vector_db = VectorStoreFactory.get_vectorstore(
        embedding=embedding,
        vectorstore=VECTORSTORE
    )

    # ---------------------------------------
    # STEP 3: Load existing FAISS index
    # ---------------------------------------

    if vector_db.exists():

        logger.info(
            "Existing vector database found. Loading..."
        )

        vector_db.load()

    else:

        logger.info(
            "No existing vector database found. "
            "A new index will be created on first document upload."
        )

    # ---------------------------------------
    # STEP 4: Create document registry
    # ---------------------------------------

    document_registry = DocumentRegistry(
        DOCUMENT_REGISTRY_PATH
    )

    # ---------------------------------------
    # STEP 5: Create RAG aservice
    # ---------------------------------------

    app.state.rag_service = RAGService(
        vector_db=vector_db
    )

    # ---------------------------------------
    # STEP 6: Create document service
    # ---------------------------------------

    app.state.document_service = DocumentService(
        vector_db=vector_db,
        document_registry=document_registry
    )

    logger.info(
        "Application services initialized successfully."
    )

    yield

    # ---------------------------------------
    # Shutdown
    # ---------------------------------------

    logger.info("Cleaning up resources...")

    logger.info(
        "Enterprise RAG API stopped."
    )


app = FastAPI(
    title="Enterprise RAG",
    version="1.0.0",
    description="Enterprise Retrieval Augmented Generation API",
    lifespan=lifespan
)


register_exception_handlers(app)

app.include_router(rag_router)
app.include_router(document_router)


@app.get("/")
def home():

    return {
        "message": "Enterprise RAG Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/version")
def version():

    return {
        "version": app.version
    }