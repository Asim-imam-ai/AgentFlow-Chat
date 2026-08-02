import json
import logging
import os

from langchain_core.tools import tool

from app.tools.registry import tool_registry

logger = logging.getLogger("agentflow.tools.memory")
MEMORY_FILE = "user_memory.json"


def load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
    return {}


def save_memory(data: dict) -> None:
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving memory: {e}")


@tool("memory")
def memory_tool(action: str, key: str, value: str | None = None) -> str:
    """
    Store or retrieve user profile facts and preferences to remember between sessions.

    Args:
        action (str): Must be either 'get', 'set', or 'delete'.
        key (str): The identifier for the memory fact (e.g., 'user_name', 'coding_preferences', 'favorite_languages').
        value (str, optional): The details to store. Required for 'set'.

    Returns:
        str: Response text indicating result of operation.
    """
    memory = load_memory()

    if action == "get":
        val = memory.get(key)
        if val:
            return f"Memory for '{key}': {val}"
        return f"No memory found for key '{key}'"

    elif action == "set":
        if not value:
            return "Error: Action 'set' requires a value."
        memory[key] = value
        save_memory(memory)
        return f"Successfully saved memory: '{key}' = '{value}'"

    elif action == "delete":
        if key in memory:
            del memory[key]
            save_memory(memory)
            return f"Successfully deleted memory for key '{key}'"
        return f"Key '{key}' not found in memory"

    else:
        return f"Error: Action '{action}' is invalid. Supported actions are 'get', 'set', and 'delete'."


# Register tool
tool_registry.register(memory_tool)
