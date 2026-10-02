import os
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException, Form

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