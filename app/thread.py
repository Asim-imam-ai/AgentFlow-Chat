import uuid
from typing import Any


def generate_thread_id() -> str:
    """Generate a unique thread identifier."""
    return str(uuid.uuid4())


def get_thread_config(thread_id: str) -> dict[str, Any]:
    """Generate the LangGraph standard thread config."""
    return {"configurable": {"thread_id": thread_id}}
