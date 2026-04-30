from typing import Dict, Any
from src.llms.llms_provider import get_llm
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Initialize LLM once (singleton style)
llm = get_llm()


def chat_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Chat Agent:
    Handles general conversation using LLM.

    Args:
        state (dict):
            {
                "user_input": str,
                "messages": list (optional)
            }

    Returns:
        dict:
            {
                "response": str
            }
    """

    try:
        user_input = state.get("user_input", "")
        messages = state.get("messages", [])

        if not user_input:
            return {"response": "⚠️ No input provided."}

        logger.info(f"💬 ChatAgent received: {user_input}")

        # ---- Build prompt (basic version) ----
        prompt = _build_prompt(user_input, messages)

        # ---- Call LLM ----
        response = llm.invoke(prompt)

        content = response.content if hasattr(response, "content") else str(response)

        logger.info("✅ ChatAgent response generated")

        return {"response": content}

    except Exception as e:
        logger.error(f"❌ ChatAgent error: {str(e)}")

        return {
            "response": "Sorry, something went wrong while processing your request."
        }


# 🔧 Helper Function
def _build_prompt(user_input: str, messages: list) -> str:
    """
    Builds a simple prompt with optional chat history.
    """

    history = ""

    if messages:
        history = "\n".join(messages)

    prompt = f"""
You are a helpful AI assistant.

Conversation history:
{history}

User: {user_input}

Answer clearly and concisely:
"""

    return prompt