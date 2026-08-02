import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.chat import ChatRequest, ChatResponse
from app.database.session import get_db
from app.services.agent_service import AgentService

logger = logging.getLogger("agentflow.routes.chat")
router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a message to the AgentFlow agent.
    If a conversation_id is provided, continues the existing chat session.
    Otherwise, starts a new thread.
    """
    logger.info(f"Received message for conversation '{request.conversation_id}'")

    agent_service = AgentService(db)
    try:
        result = agent_service.execute_agent_turn(
            message=request.message,
            conversation_id=request.conversation_id,
            provider=request.provider,
            model_name=request.model_name,
            temperature=request.temperature,
        )
        return ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            summary=result["summary"],
        )
    except Exception as e:
        logger.error(f"Error during agent turn execution: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {e!s}",
        )
