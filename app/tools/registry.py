import logging

from langchain_core.tools import BaseTool

logger = logging.getLogger("agentflow.tools.registry")


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool in the registry."""
        logger.info(f"Registering tool: {tool.name}")
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseTool | None:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_all_tools(self) -> list[BaseTool]:
        """Get all registered tools."""
        return list(self._tools.values())


# Create a global instance
tool_registry = ToolRegistry()


def register_tool(tool: BaseTool) -> BaseTool:
    """Decorator to register tools directly."""
    tool_registry.register(tool)
    return tool
