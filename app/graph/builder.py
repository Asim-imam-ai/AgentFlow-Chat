from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.graph.nodes.chatbot import chatbot_node
from app.graph.nodes.tools import get_tools_node
from app.graph.nodes.memory import memory_node
from app.graph.nodes.rag import rag_node
from app.graph.nodes.summarizer import summarizer_node
from app.graph.checkpoint import get_checkpointer
import logging

logger = logging.getLogger("agentflow.graph.builder")

def should_continue(state: AgentState) -> str:
    """
    Conditional edge function that decides whether to execute tools or stop.
    """
    messages = state.get("messages", [])
    if not messages:
        return END
        
    last_message = messages[-1]
    
    # If the LLM made tool calls, run the tools node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        logger.info(f"Tool calls detected: {[tc['name'] for tc in last_message.tool_calls]}. Routing to tools.")
        return "tools"
        
    logger.info("No tool calls. Ending conversation turn.")
    return END

def build_agent_graph():
    """
    Builds and compiles the LangGraph agent state graph.
    """
    logger.info("Building StateGraph...")
    
    # 1. Initialize StateGraph
    workflow = StateGraph(AgentState)
    
    # 2. Register all nodes
    workflow.add_node("memory", memory_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("chatbot", chatbot_node)
    workflow.add_node("tools", get_tools_node())
    
    # 3. Define the connections / flow
    workflow.add_edge(START, "memory")
    workflow.add_edge("memory", "rag")
    workflow.add_edge("rag", "summarizer")
    workflow.add_edge("summarizer", "chatbot")
    
    # Add conditional router from chatbot
    workflow.add_conditional_edges(
        "chatbot",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # Route back to chatbot after running tools
    workflow.add_edge("tools", "chatbot")
    
    # 4. Compile with checkpointer
    checkpointer = get_checkpointer()
    compiled_graph = workflow.compile(checkpointer=checkpointer)
    
    logger.info("Agent StateGraph compiled successfully.")
    return compiled_graph
