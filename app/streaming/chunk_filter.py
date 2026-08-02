from typing import Any


class ChunkFilter:
    """Utility to filter and format streaming updates from LangGraph.
    Only yields content updates from specific nodes (e.g., chatbot replies).
    """

    def filter_update(self, update: dict[str, Any]) -> dict[str, Any] | None:
        """Parses update events from graph nodes.
        Returns clean token/text content if chatbot is generating text.
        """
        # Updates are in format: {node_name: {state_keys: values}}
        for node_name, node_output in update.items():
            if node_name == "chatbot":
                messages = node_output.get("messages", [])
                if messages:
                    last_msg = messages[-1]
                    # Check if it has content
                    if hasattr(last_msg, "content") and last_msg.content:
                        return {
                            "node": node_name,
                            "type": "content",
                            "content": last_msg.content,
                        }
            elif node_name == "tools":
                # Report tool execution info to the user
                messages = node_output.get("messages", [])
                if messages:
                    last_msg = messages[-1]
                    return {
                        "node": node_name,
                        "type": "tool_result",
                        "content": last_msg.content,
                        "tool_name": getattr(last_msg, "name", "unknown"),
                    }
        return None
