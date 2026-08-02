import logging

from fastapi import APIRouter, File, Form, UploadFile

from app.api.schemas.upload import UploadResponse
from app.services.upload_service import upload_service

logger = logging.getLogger("agentflow.routes.upload")
router = APIRouter(tags=["Document Management"])


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    conversation_id: str | None = Form(None),
):
    """
    Upload a document and immediately index it into the RAG vector store.

    The ``conversation_id`` form field scopes the document to a specific
    conversation thread so that retrieval only returns chunks relevant to
    the active conversation.

    Supported formats: .txt, .md, .csv, .pdf
    """
    logger.info(
        f"[UPLOAD] filename='{file.filename}'  "
        f"content_type='{file.content_type}'  "
        f"conversation_id='{conversation_id}'"
    )

    stats = await upload_service.process_upload(
        file=file,
        conversation_id=conversation_id,
    )

    return UploadResponse(
        filename=stats["filename"],
        content_type=file.content_type or "application/octet-stream",
        size_bytes=stats["size_bytes"],
        message=(
            f"File '{stats['filename']}' uploaded and indexed successfully. "
            f"Extracted {stats['text_length']} characters, "
            f"created {stats['chunks']} chunks / embeddings."
        ),
        text_length=stats["text_length"],
        chunks=stats["chunks"],
        embeddings=stats["embeddings"],
        conversation_id=conversation_id,
    )
