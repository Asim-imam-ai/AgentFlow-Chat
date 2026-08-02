from pydantic import BaseModel, Field


class MessageDetail(BaseModel):
    role: str = Field(
        ...,
        description="Role of the message sender ('user', 'assistant', 'system', 'tool').",
    )
    content: str = Field(..., description="Text content of the message.")
    id: str | None = Field(None, description="Unique ID of the message.")


class HistoryResponse(BaseModel):
    conversation_id: str = Field(..., description="The session/thread identifier.")
    summary: str | None = Field(None, description="The current conversation summary.")
    messages: list[MessageDetail] = Field(
        ...,
        description="List of messages in the chat history.",
    )
