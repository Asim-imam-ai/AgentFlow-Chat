from pydantic import BaseModel, Field


class ConversationInfo(BaseModel):
    conversation_id: str = Field(
        ..., description="The unique session/thread identifier."
    )
    message_count: int = Field(
        ..., description="Total number of messages in the thread."
    )
    summary: str | None = Field(
        None, description="The current summary of this conversation."
    )


class ConversationListResponse(BaseModel):
    conversations: list[ConversationInfo] = Field(
        ..., description="List of all active or stored conversations."
    )
