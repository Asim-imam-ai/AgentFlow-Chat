from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user message to send to the chatbot.")
    conversation_id: Optional[str] = Field(None, description="The unique session/thread ID. Generates a new one if not provided.")
    provider: Optional[str] = Field(None, description="LLM provider: 'openai' or 'gemini'.")
    model_name: Optional[str] = Field(None, description="Specific model name to use.")
    temperature: Optional[float] = Field(None, description="Creativity temperature (0.0 to 1.0).", ge=0.0, le=1.0)

class ChatResponse(BaseModel):
    response: str = Field(..., description="The assistant's text response.")
    conversation_id: str = Field(..., description="The thread/session ID associated with this turn.")
    summary: Optional[str] = Field(None, description="The current summary of the conversation.")
