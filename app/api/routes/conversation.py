import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.conversation import ConversationInfo, ConversationListResponse
from app.database.session import get_db
from app.services.conversation_service import ConversationService

logger = logging.getLogger("agentflow.routes.conversation")
router = APIRouter(tags=["Conversations"])


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(db: Session = Depends(get_db)):
    """
    List all active conversation sessions/threads and their current metadata.
    """
    try:
        service = ConversationService(db)
        conversations = service.list_all_conversations()

        formatted = []
        for conv in conversations:
            formatted.append(
                ConversationInfo(
                    conversation_id=conv.conversation_id,
                    message_count=conv.message_count,
                    summary=conv.summary,
                )
            )
        return ConversationListResponse(conversations=formatted)
    except Exception as e:
        logger.error(f"Error listing conversations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list conversation sessions: {e!s}",
        )
