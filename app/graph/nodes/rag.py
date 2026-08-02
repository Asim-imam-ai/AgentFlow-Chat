import logging

from app.graph.state import AgentState
from app.services.rag_service import rag_service_wrapper

logger = logging.getLogger("agentflow.graph.nodes.rag")

_RAG_CHUNK_LIMIT = 4


def rag_node(state: AgentState) -> dict:
    """RAG pre-retrieval node.

    Runs *before* the chatbot node and injects relevant document context into
    ``state['rag_context']``.  Retrieval is scoped to the active conversation
    via ``state['conversation_id']``, so only documents uploaded for this
    specific thread are considered.

    If no documents have been indexed for the conversation yet, ``rag_context``
    is set to an empty string and the chatbot will answer from its own knowledge.
    """
    logger.info("[RAG NODE] Starting pre-retrieval step.")

    conversation_id = state.get("conversation_id")
    messages = state.get("messages", [])

    # Extract the latest user message as the retrieval query
    query = ""
    for msg in reversed(messages):
        content = getattr(msg, "content", None)
        if content and hasattr(msg, "type") and msg.type == "human":
            query = content
            break
        # Fallback: check __class__ name for compatibility
        if content and msg.__class__.__name__ == "HumanMessage":
            query = content
            break

    if not query:
        logger.info("[RAG NODE] No human message found — skipping retrieval.")
        return {"rag_context": ""}

    logger.info(
        f"[RAG NODE] Retrieving for query='{query[:80]}…'  conversation_id='{conversation_id}'",
    )

    chunks = rag_service_wrapper.search_documents(
        query=query,
        conversation_id=conversation_id,
        limit=_RAG_CHUNK_LIMIT,
    )

    if not chunks:
        logger.warning(
            f"[RAG NODE] No document chunks retrieved for conversation_id='{conversation_id}'. "
            "The chatbot will answer without document context.",
        )
        return {"rag_context": ""}

    # Format chunks into a readable context block for the chatbot prompt
    parts = []
    for i, chunk in enumerate(chunks, start=1):
        source = chunk["metadata"].get("source", "unknown")
        parts.append(f"[Chunk {i} — source: {source}]\n{chunk['content']}")

    rag_context = "\n\n---\n\n".join(parts)

    logger.info(
        f"[RAG NODE] Injecting {len(chunks)} chunk(s) as rag_context. "
        f"doc_ids={[c['doc_id'] for c in chunks]}",
    )

    return {"rag_context": rag_context}
