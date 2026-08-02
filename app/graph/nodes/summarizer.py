import logging

from langchain_core.messages import HumanMessage, RemoveMessage
from langchain_openai import ChatOpenAI

from app.core.prompts import SUMMARIZER_PROMPT
from app.core.settings import settings
from app.graph.state import AgentState
from app.llms.gemini import get_gemini_llm

logger = logging.getLogger("agentflow.graph.nodes.summarizer")


def summarizer_node(state: AgentState) -> dict:
    """Summarizes the conversation history if it gets too long,
    storing the summary in the state and removing older messages.
    """
    messages = state.get("messages", [])

    # Only summarize if we have more than 6 messages (3 turns)
    if len(messages) <= 6:
        return {}

    logger.info(
        f"Conversation length ({len(messages)}) exceeds limit. Generating summary...",
    )

    # 1. Prepare messages for summary
    existing_summary = state.get("summary", "")

    # We will summarize all but the last 2 messages (the last user message and assistant message)
    messages_to_summarize = messages[:-2]
    messages_to_keep = messages[-2:]

    formatted_messages = []
    for msg in messages_to_summarize:
        role = "User" if isinstance(msg, HumanMessage) else "Assistant"
        formatted_messages.append(f"{role}: {msg.content}")

    new_messages_str = "\n".join(formatted_messages)

    # 2. Call LLM to summarize
    provider = state.get("provider") or settings.DEFAULT_LLM_PROVIDER
    if provider == "gemini":
        llm = get_gemini_llm()
    else:
        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0,
            api_key=settings.OPENAI_API_KEY,
        )

    prompt = SUMMARIZER_PROMPT.format(
        existing_summary=existing_summary,
        new_messages=new_messages_str,
    )

    response = llm.invoke(prompt)
    summary_text = response.content if hasattr(response, "content") else str(response)

    logger.info("Successfully created new conversation summary.")

    # 3. Create RemoveMessage objects for messages we are summarizing
    # This deletes them from the LangGraph state
    delete_messages = [RemoveMessage(id=msg.id) for msg in messages_to_summarize if msg.id]

    return {"summary": summary_text, "messages": delete_messages}
