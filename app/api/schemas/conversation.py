from pydantic import BaseModel, Field
from typing import List, Optional

class ConversationInfo(BaseModel):
    conversation_id: str = Field(..., description="The unique session/thread identifier.")
    message_count: int = Field(..., description="Total number of messages in the thread.")
    summary: Optional[str] = Field(None, description="The current summary of this conversation.")

class ConversationListResponse(BaseModel):
    conversations: List[ConversationInfo] = Field(..., description="List of all active or stored conversations.")
