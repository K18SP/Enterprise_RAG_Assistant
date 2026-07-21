from fastapi import FastAPI

# Initialize FastAPI application with metadata
app = FastAPI(
    title = "Enterprise RAG",
    version = "1.0"
) 

# HTTP GET route decorator for the root path
@app.get("/") 
def home():

    # Return a JSON response confirming status
    return {
        "message" : "Enterprise RAG Running"
    }