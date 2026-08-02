from app.graph.state import AgentState
from app.core.settings import settings
from app.core.prompts import CHATBOT_SYSTEM_PROMPT
from app.llms.gemini import get_gemini_llm
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from app.tools.registry import tool_registry
import logging

logger = logging.getLogger("agentflow.graph.nodes.chatbot")


def chatbot_node(state: AgentState) -> dict:
    """
    Chatbot node that interacts with the LLM.

    Consumes:
      - state['rag_context']    — document snippets retrieved by the RAG node
      - state['memory_context'] — user memory facts
      - state['summary']        — rolling conversation summary
    """
    logger.info("Executing chatbot node")

    # 1. Determine provider & model
    provider = state.get("provider") or settings.DEFAULT_LLM_PROVIDER
    model_name = state.get("model_name")
    temp = state.get("temperature") if state.get("temperature") is not None else settings.TEMPERATURE

    # 2. Get LLM instance
    if provider == "gemini":
        model_name = model_name or settings.GEMINI_MODEL
        llm = get_gemini_llm(model_name=model_name, temperature=temp)
    else:
        model_name = model_name or settings.OPENAI_MODEL
        llm = ChatOpenAI(
            model=model_name,
            temperature=temp,
            api_key=settings.OPENAI_API_KEY
        )

    # 3. Bind tools
    tools = tool_registry.get_all_tools()
    llm_with_tools = llm.bind_tools(tools)

    # 4. Construct prompt with context
    memory_ctx = state.get("memory_context") or "No personal details saved yet."
    summary_ctx = state.get("summary") or "No previous history summary."
    rag_ctx = state.get("rag_context") or ""

    system_prompt = CHATBOT_SYSTEM_PROMPT.format(
        memory_context=memory_ctx,
        summary_context=summary_ctx,
        rag_context=rag_ctx,
    )

    if rag_ctx:
        logger.info(
            f"[CHATBOT NODE] Injecting RAG context ({len(rag_ctx)} chars) into system prompt."
        )
    else:
        logger.info("[CHATBOT NODE] No RAG context available — answering from model knowledge.")

    system_message = SystemMessage(content=system_prompt)

    # 5. Invoke model
    messages = [system_message] + state["messages"]
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}
