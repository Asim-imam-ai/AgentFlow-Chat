from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    # The messages list will append new messages automatically
    messages: Annotated[List[BaseMessage], add_messages]

    # Conversation summary (rolling, updated by summarizer node)
    summary: str

    # Memory facts context (injected by memory node)
    memory_context: str

    # RAG context injected by the rag node before chatbot runs
    rag_context: str

    # The active conversation/thread ID — needed by the RAG node to scope retrieval
    conversation_id: Optional[str]

    # Optional planner fields
    planner_steps: List[str]
    current_step_index: int

    # Provider / model overrides passed in from the API layer
    provider: str
    model_name: str
    temperature: float
