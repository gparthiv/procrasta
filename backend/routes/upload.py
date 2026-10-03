import os
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from qdrant_client.models import Filter, FieldCondition, MatchValue
from rag.resources import qdrant_client, COLLECTION_NAME
from client.rq_client import ingestion_queue
from rag.ingestion import process_upload
from session import refresh_session

router = APIRouter()

MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Form(...),
):

    if not refresh_session(user_id):
        raise HTTPException(
            status_code=401,
            detail="Session expired.",
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum size is 20 MB.",
        )

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as tmp:

        tmp.write(contents)
        file_path = tmp.name

    job = ingestion_queue.enqueue(
        process_upload,
        file_path,
        file.filename,
        user_id,
    )

    return {
        "status": "queued",
        "job_id": job.id,
        "filename": file.filename,
        "user_id": user_id,
    }


@router.get("/files/{user_id}")
async def get_user_files(user_id: str):
    if not refresh_session(user_id):
        raise HTTPException(status_code=401, detail="Session expired.")

    result, _ = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="metadata.user_id",
                    match=MatchValue(value=user_id),
                )
            ]
        ),
        limit=100,
        with_payload=True,
        with_vectors=False,
    )

    files = set()

    for point in result:
        metadata = point.payload.get("metadata", {})
        source = metadata.get("source")

        if source:
            files.add(source)

    return {"files": sorted(files)}
