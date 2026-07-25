from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(
    title="Enterprise RAG Assistant",
    version = '1.0.0',
    description = 'Enterprise RAG API'
)

app.include_router(router)