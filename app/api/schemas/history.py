from pydantic import BaseModel, Field
from typing import List, Optional

class MessageDetail(BaseModel):
    role: str = Field(..., description="Role of the message sender ('user', 'assistant', 'system', 'tool').")
    content: str = Field(..., description="Text content of the message.")
    id: Optional[str] = Field(None, description="Unique ID of the message.")

class HistoryResponse(BaseModel):
    conversation_id: str = Field(..., description="The session/thread identifier.")
    summary: Optional[str] = Field(None, description="The current conversation summary.")
    messages: List[MessageDetail] = Field(..., description="List of messages in the chat history.")
