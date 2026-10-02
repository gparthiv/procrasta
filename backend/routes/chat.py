from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from rag.chat import process_query
from rag.resources import vector_store

from client.rq_client import chat_queue

from rq.job import Job
from client.rq_client import redis_connection

from qdrant_client.models import Filter, FieldCondition, MatchValue

router = APIRouter()

from session import refresh_session


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=2)
    user_id: str = Field(..., min_length=1)


@router.post("/search")
async def search_endpoint(req: ChatRequest):
    results = vector_store.similarity_search(
        req.query,
        k=3,
        filter=Filter(
            must=[
                FieldCondition(
                    key="metadata.user_id",
                    match=MatchValue(value=req.user_id),
                )
            ]
        ),
    )

    return {
        "query": req.query,
        "user_id": req.user_id,
        "results": [
            {
                "text": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in results
        ],
    }


@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    if not refresh_session(req.user_id):
        raise HTTPException(
            status_code=401,
            detail="Session expired.",
        )
    job = chat_queue.enqueue(
        process_query,
        req.query,
        req.user_id,
    )

    return {
        "status": "queued",
        "job_id": job.id,
    }


@router.get("/job/{job_id}")
async def get_job_status(job_id: str):

    job = Job.fetch(
        job_id,
        connection=redis_connection,
    )

    if job.is_finished:

        return {
            "status": "completed",
            "job_id": job.id,
            "result": job.return_value(),
        }

    if job.is_failed:

        return {
            "status": "failed",
            "job_id": job.id,
            "error": str(job.exc_info),
        }

    if job.is_started:

        return {
            "status": "processing",
            "job_id": job.id,
        }

    return {
        "status": "queued",
        "job_id": job.id,
    }
