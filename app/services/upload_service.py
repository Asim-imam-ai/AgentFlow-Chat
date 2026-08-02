import logging
import os
import shutil

from fastapi import HTTPException, UploadFile, status

from app.core.settings import settings
from app.services.rag_service import rag_service_wrapper

logger = logging.getLogger("agentflow.services.upload_service")


class UploadService:
    async def process_upload(
        self,
        file: UploadFile,
        conversation_id: str | None = None,
    ) -> dict:
        """
        Save the uploaded file to disk and trigger RAG ingestion.

        Args:
            file:             The FastAPI UploadFile object.
            conversation_id:  Scopes the indexed chunks to this conversation.

        Returns:
            Stats dict: {filename, size_bytes, text_length, chunks, embeddings, conversation_id}
        """
        if not os.path.exists(settings.UPLOAD_DIR):
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        # Guard against path traversal
        safe_name = os.path.basename(file.filename or "upload")
        file_path = os.path.join(settings.UPLOAD_DIR, safe_name)

        try:
            # ── 1. Save file to disk ──────────────────────────────────────
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            size_bytes = os.path.getsize(file_path)
            logger.info(
                f"[UPLOAD SERVICE] Saved '{safe_name}' ({size_bytes} bytes). "
                f"Triggering RAG ingestion for conversation_id='{conversation_id}'…"
            )

            # ── 2. Ingest into vector store ───────────────────────────────
            stats = rag_service_wrapper.ingest_document(
                file_path=file_path,
                conversation_id=conversation_id,
            )

            stats["size_bytes"] = size_bytes
            logger.info(
                f"[UPLOAD SERVICE] Ingestion complete: "
                f"filename='{stats['filename']}'  "
                f"text_length={stats['text_length']}  "
                f"chunks={stats['chunks']}  "
                f"embeddings={stats['embeddings']}  "
                f"conversation_id='{conversation_id}'"
            )
            return stats

        except Exception as e:
            logger.error(f"[UPLOAD SERVICE] Error saving/indexing '{safe_name}': {e}")
            # Clean up partial file on failure
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    pass
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Upload/indexing failed: {e!s}",
            )


upload_service = UploadService()
