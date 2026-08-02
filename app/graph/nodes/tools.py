from langgraph.prebuilt import ToolNode

from app.tools.registry import tool_registry


def get_tools_node() -> ToolNode:
    """Returns a ToolNode configured with all registered tools from the tool registry."""
    tools = tool_registry.get_all_tools()
    return ToolNode(tools)
