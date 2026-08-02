import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.response import GenericResponse
from app.database.session import get_db
from app.services.conversation_service import ConversationService

logger = logging.getLogger("agentflow.routes.thread")
router = APIRouter(tags=["Thread Management"])


@router.post("/thread/new", response_model=GenericResponse)
async def create_new_thread(db: Session = Depends(get_db)):
    """Generate a new unique thread/session identifier for conversation mapping and save it in SQLite."""
    new_id = str(uuid.uuid4())
    logger.info(f"Generated new thread ID: {new_id}")

    try:
        service = ConversationService(db)
        service.create_conversation(new_id)
        return GenericResponse(
            success=True,
            message="New thread generated successfully.",
            data={"thread_id": new_id},
        )
    except Exception as e:
        logger.error(f"Failed to create new thread: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create thread: {e!s}",
        )


@router.post("/thread/{thread_id}/clear", response_model=GenericResponse)
async def clear_thread(thread_id: str, db: Session = Depends(get_db)):
    """Clear/delete all conversation data for a thread from the database."""
    try:
        service = ConversationService(db)
        success = service.delete_conversation(thread_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation '{thread_id}' not found.",
            )

        logger.info(f"Cleared thread state for thread '{thread_id}'")
        return GenericResponse(
            success=True,
            message=f"Successfully cleared thread '{thread_id}' conversation data.",
            data={"thread_id": thread_id},
        )
    except Exception as e:
        logger.error(f"Failed to clear thread: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear thread data: {e!s}",
        )


@router.post("/thread/{thread_id}/rename", response_model=GenericResponse)
async def rename_thread(thread_id: str, summary: str, db: Session = Depends(get_db)):
    """Rename a conversation thread summary."""
    try:
        service = ConversationService(db)
        conv = service.create_or_update_summary(thread_id, summary)
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation '{thread_id}' not found.",
            )
        logger.info(f"Renamed thread '{thread_id}' to '{summary}'")
        return GenericResponse(
            success=True,
            message="Conversation renamed successfully.",
            data={"thread_id": thread_id, "summary": summary},
        )
    except Exception as e:
        logger.error(f"Failed to rename thread: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rename thread: {e!s}",
        )
