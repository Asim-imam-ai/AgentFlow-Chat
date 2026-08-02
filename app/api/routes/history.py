import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.history import HistoryResponse, MessageDetail
from app.database.session import get_db
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService

logger = logging.getLogger("agentflow.routes.history")
router = APIRouter(tags=["History"])


@router.get("/history/{conversation_id}", response_model=HistoryResponse)
async def get_conversation_history(conversation_id: str, db: Session = Depends(get_db)):
    """
    Get the complete message history and summary for a conversation/thread session.
    """
    try:
        conversation_service = ConversationService(db)
        chat_service = ChatService(db)

        conv = conversation_service.get_conversation(conversation_id)
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation session '{conversation_id}' not found.",
            )

        messages = chat_service.get_chat_history(conversation_id)
        summary = conv.summary

        formatted_messages = []
        for msg in messages:
            formatted_messages.append(
                MessageDetail(role=msg.role, content=msg.content, id=str(msg.id))
            )

        return HistoryResponse(
            conversation_id=conversation_id,
            summary=summary,
            messages=formatted_messages,
        )
    except Exception as e:
        logger.error(f"Error fetching conversation history: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving history: {e!s}",
        )
