from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import router
from api.exception_handlers import register_exception_handlers

from services.rag_service import RAGService

from utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting Enterprise RAG API...")

    app.state.rag_service = RAGService()

    yield

    logger.info("Cleaning up resources...")

    # Example:
    # app.state.redis.close()
    # app.state.qdrant_client.close()

    logger.info("Enterprise RAG API stopped.")


app = FastAPI(
    title="Enterprise RAG",
    version="1.0.0",
    description="Enterprise Retrieval Augmented Generation API",
    lifespan=lifespan
)

register_exception_handlers(app)

app.include_router(router)


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