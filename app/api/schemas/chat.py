from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="The user message to send to the chatbot.")
    conversation_id: str | None = Field(
        None,
        description="The unique session/thread ID. Generates a new one if not provided.",
    )
    provider: str | None = Field(
        None, description="LLM provider: 'openai' or 'gemini'."
    )
    model_name: str | None = Field(None, description="Specific model name to use.")
    temperature: float | None = Field(
        None, description="Creativity temperature (0.0 to 1.0).", ge=0.0, le=1.0
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="The assistant's text response.")
    conversation_id: str = Field(
        ..., description="The thread/session ID associated with this turn."
    )
    summary: str | None = Field(
        None, description="The current summary of the conversation."
    )
