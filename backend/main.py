from fastapi import FastAPI
from fastapi import HTTPException
from rag.cleanup import delete_user_data
from rag.resources import qdrant_client, COLLECTION_NAME
from config import valkey_client
from session import create_session
from routes.chat import router as chat_router
from routes.upload import router as upload_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ProCrasto")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(upload_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/test-embedding")
def test_embedding():
    from rag.resources import embeddings

    text = "CPU scheduling is the process " "of selecting a process for execution."

    vector = embeddings.embed_query(text)

    return {
        "status": "success",
        "dimensions": len(vector),
        "first_10_values": vector[:10],
    }


@app.get("/cache-test")
def cache_test():

    valkey_client.set(
        "status",
        "running",
    )

    result = valkey_client.get("status")

    return {"valkey_status": result}


@app.delete("/cleanup/{user_id}")
def cleanup_user(user_id: str):
    return delete_user_data(user_id)


@app.post("/session")
def create_new_session():
    user_id = create_session()

    return {
        "user_id": user_id,
        "expires_in": 3600,
    }
