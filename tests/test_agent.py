from langchain_core.messages import AIMessage, HumanMessage

from app.graph.builder import should_continue
from app.graph.state import AgentState


def test_should_continue_logic():
    """Test routing conditional edge in StateGraph."""
    # State with no tool calls should END
    state_no_tools: AgentState = {
        "messages": [HumanMessage(content="Hello"), AIMessage(content="Hi!")],
        "summary": "",
        "memory_context": "",
        "planner_steps": [],
        "current_step_index": 0,
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "temperature": 0.7,
    }
    assert should_continue(state_no_tools) == "__end__"

    # State with tool calls should route to tools node
    ai_msg_with_tool = AIMessage(content="")
    ai_msg_with_tool.tool_calls = [
        {"name": "web_search", "args": {"query": "test"}, "id": "call-1"},
    ]

    state_with_tools: AgentState = {
        "messages": [HumanMessage(content="Search for test"), ai_msg_with_tool],
        "summary": "",
        "memory_context": "",
        "planner_steps": [],
        "current_step_index": 0,
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "temperature": 0.7,
    }
    assert should_continue(state_with_tools) == "tools"
