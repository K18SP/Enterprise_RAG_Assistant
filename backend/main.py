from fastapi import FastAPI
from api.routes import router

# Initialize FastAPI application with metadata
app = FastAPI(
    title = "Enterprise RAG",
    version = "1.0",
    description="Enterprise-grade Retrieval Augmented Generation API"
) 

# HTTP GET route decorator for the root path
@app.get("/") 
def home():

    # Return a JSON response confirming status
    return {
        "message" : "Enterprise RAG Running"
    }

app.include_router(router)