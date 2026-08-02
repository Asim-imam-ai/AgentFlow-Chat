from typing import Any


class ResponseBuilder:
    """
    Accumulates streaming chunks to construct the final compiled response object.
    Useful for building final logs or verifying stream consistency.
    """

    def __init__(self):
        self._content_parts: list[str] = []
        self._tool_calls: list[dict[str, Any]] = []

    def append_chunk(self, chunk: dict[str, Any]) -> None:
        """
        Record a chunk output.
        """
        chunk_type = chunk.get("type")
        if chunk_type == "content":
            self._content_parts.append(chunk.get("content", ""))
        elif chunk_type == "tool_result":
            self._tool_calls.append(
                {"tool": chunk.get("tool_name"), "result": chunk.get("content")}
            )

    def get_final_response(self) -> dict[str, Any]:
        """
        Returns the aggregated response.
        """
        return {
            "response": "".join(self._content_parts),
            "tool_calls": self._tool_calls,
        }
