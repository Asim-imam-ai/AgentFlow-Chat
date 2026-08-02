from typing import Dict, Any, List, Callable
from langchain_core.tools import BaseTool
import logging

logger = logging.getLogger("agentflow.tools.registry")

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool in the registry."""
        logger.info(f"Registering tool: {tool.name}")
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseTool | None:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools."""
        return list(self._tools.values())

# Create a global instance
tool_registry = ToolRegistry()

def register_tool(tool: BaseTool) -> BaseTool:
    """Decorator to register tools directly."""
    tool_registry.register(tool)
    return tool
