from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import router as rag_router
from api.document_routes import router as document_router
from api.exception_handlers import register_exception_handlers

from embeddings.embedding_factory import EmbeddingFactory
from vectordb.vectorstore_factory import VectorStoreFactory

from services.user_workspace import UserWorkspace
from services.document_registry import DocumentRegistry
from services.document_service import DocumentService
from services.rag_service import RAGService

from config.constants import (
    EMBEDDING_PROVIDER,
    VECTORSTORE
)

from utils.logger import setup_logger


logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting Enterprise RAG API...")

    # ---------------------------------------
    # STEP 1 : Create User Workspace
    # ---------------------------------------

    # Later:
    # workspace = UserWorkspace(current_user.username)

    workspace = UserWorkspace("default")

    # ---------------------------------------
    # STEP 2 : Create Embedding Model
    # ---------------------------------------

    embedding = EmbeddingFactory.get_embedding(
        EMBEDDING_PROVIDER
    )

    # ---------------------------------------
    # STEP 3 : Create User Vector Database
    # ---------------------------------------

    vector_db = VectorStoreFactory.get_vectorstore(

        embedding=embedding,

        vectorstore=VECTORSTORE,

        save_path=workspace.vector_db_path

    )

    # ---------------------------------------
    # STEP 4 : Load Existing FAISS
    # ---------------------------------------

    if vector_db.exists():

        logger.info(
            "Existing vector database found. Loading..."
        )

        vector_db.load()

    else:

        logger.info(
            "No vector database found. "
            "A new index will be created after first upload."
        )

    # ---------------------------------------
    # STEP 5 : Create Document Registry
    # ---------------------------------------

    document_registry = DocumentRegistry(

        workspace.registry_path

    )

    # ---------------------------------------
    # STEP 6 : Create Services
    # ---------------------------------------

    app.state.rag_service = RAGService(

        vector_db=vector_db

    )

    app.state.document_service = DocumentService(

        vector_db=vector_db,

        document_registry=document_registry,

        workspace=workspace

    )

    logger.info(
        "Application services initialized successfully."
    )

    yield

    # ---------------------------------------
    # Shutdown
    # ---------------------------------------

    logger.info(
        "Cleaning up resources..."
    )

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