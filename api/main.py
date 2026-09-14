from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    BackgroundTasks,
    HTTPException,
    Request
)
from fastapi import HTTPException
from langchain_core.messages import HumanMessage, AIMessage

from api.schemas import QuestionRequest

from services.ingestion_service import (
    process_document_in_background,
    job_status,
    chain_store,
    chat_history_store
)

from langchain_core.messages import HumanMessage, AIMessage

import uuid

from fastapi import Request
from fastapi.responses import JSONResponse

from api.rate_limiter import is_rate_limited



app = FastAPI(
    title="DocuMind AI API",
    description="Backend API for document-based question answering",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to DocuMind AI API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/documents/upload")
async def upload_document(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(None),
    source_url: str = Form(None)
):
    """
    Accepts either:
    - An uploaded PDF, CSV, or TXT file
    - A webpage URL
    """

    client_ip = request.client.host

    if is_rate_limited(
        client_id=f"upload:{client_ip}",
        limit=10,
        window_seconds=60
    ):
        raise HTTPException(
            status_code=429,
            detail="Too many uploads. Try again later."
        )

    if file is None and not source_url:
        raise HTTPException(
            status_code=400,
            detail="Provide either a file or a source URL."
        )

    if file is not None and source_url:
        raise HTTPException(
            status_code=400,
            detail="Provide only one source: file or URL."
        )

    job_id = str(uuid.uuid4())

    if source_url:

        filename = source_url

        job_status[job_id] = {
            "status": "queued",
            "filename": filename
        }

        background_tasks.add_task(
            process_document_in_background,
            job_id,
            filename,
            None,
            source_url
        )

        return {
            "job_id": job_id,
            "message": "URL ingestion started."
        }

    filename = file.filename
    content = await file.read()

    job_status[job_id] = {
        "status": "queued",
        "filename": filename
    }

    background_tasks.add_task(
        process_document_in_background,
        job_id,
        filename,
        content,
        None
    )

    return {
        "job_id": job_id,
        "message": "File ingestion started."
    }



@app.get("/documents/status/{job_id}")
def get_document_status(job_id: str):

    if job_id not in job_status:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job_status[job_id]



@app.post("/questions/ask")
def ask_question(
    request: Request,
    question_request: QuestionRequest
):
    client_ip = request.client.host

    if is_rate_limited(
        client_id=f"question:{client_ip}",
        limit=5,
        window_seconds=60
    ):
        raise HTTPException(
            status_code=429,
            detail="Too many questions. Try again later."
        )

    job_id = question_request.job_id

    if job_id not in job_status:
        raise HTTPException(
            status_code=404,
            detail="Document job not found."
        )

    if job_status[job_id]["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail="Document is not ready yet."
        )

    chain = chain_store.get(job_id)

    if chain is None:
        raise HTTPException(
            status_code=404,
            detail="RAG chain not found."
        )

    if job_id not in chat_history_store:
        chat_history_store[job_id] = []

    current_history = chat_history_store[job_id]

    try:
        result = chain.invoke(
            {
                "input": question_request.question,
                "chat_history": current_history
            }
        )

        answer = result.get(
            "answer",
            "No answer was generated."
        )

        current_history.append(
            HumanMessage(
                content=question_request.question
            )
        )

        current_history.append(
            AIMessage(content=answer)
        )

        return {
            "job_id": job_id,
            "question": question_request.question,
            "answer": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Question processing failed: {str(error)}"
        )