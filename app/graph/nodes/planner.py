import logging

from langchain_openai import ChatOpenAI

from app.core.prompts import PLANNER_SYSTEM_PROMPT
from app.core.settings import settings
from app.graph.state import AgentState
from app.llms.gemini import get_gemini_llm

logger = logging.getLogger("agentflow.graph.nodes.planner")


def planner_node(state: AgentState) -> dict:
    """Optional planner node. Creates a plan of execution for complex tasks."""
    logger.info("Executing planner node")

    # Simple check: only plan if there are no planner steps
    if state.get("planner_steps"):
        return {}

    user_input = ""
    # Find last user message
    for msg in reversed(state["messages"]):
        if msg.type == "user":
            user_input = msg.content
            break

    if not user_input:
        return {}

    provider = state.get("provider") or settings.DEFAULT_LLM_PROVIDER
    if provider == "gemini":
        llm = get_gemini_llm()
    else:
        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0,
            api_key=settings.OPENAI_API_KEY,
        )

    prompt = PLANNER_SYSTEM_PROMPT.format(user_input=user_input)
    response = llm.invoke(prompt)

    steps = [step.strip() for step in response.content.split("\n") if step.strip()]
    logger.info(f"Generated plan: {steps}")

    return {"planner_steps": steps, "current_step_index": 0}
