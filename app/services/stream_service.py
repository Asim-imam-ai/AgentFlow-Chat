import json
import logging
from collections.abc import AsyncGenerator

from langchain_core.messages import HumanMessage

from app.graph.factory import get_graph

logger = logging.getLogger("agentflow.services.stream_service")


class StreamService:
    async def stream_chat(
        self,
        message: str,
        conversation_id: str,
        provider: str = None,
        model_name: str = None,
    ) -> AsyncGenerator[str, None]:
        """Stream agent events token-by-token or state-by-state."""
        graph = get_graph()
        config = {"configurable": {"thread_id": conversation_id}}

        inputs = {"messages": [HumanMessage(content=message)]}
        if provider:
            inputs["provider"] = provider
        if model_name:
            inputs["model_name"] = model_name

        logger.info(f"Streaming chat for thread '{conversation_id}'")

        # We use graph.astream_events or graph.astream to stream
        try:
            async for event in graph.astream(inputs, config, stream_mode="updates"):
                # Format update event to SSE (Server-Sent Events)
                # Event yields a dict representing which node finished and its state output
                yield f"data: {json.dumps(event)}\n\n"

            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"Streaming error on thread {conversation_id}: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"


stream_service = StreamService()
