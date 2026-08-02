import logging
from typing import Any

from app.rag.vectorstore import persistent_vector_store

logger = logging.getLogger("agentflow.rag.retrieval")


class DocumentRetriever:
    def __init__(self, k: int = 4):
        self.k = k

    def retrieve(
        self,
        query: str,
        conversation_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search the vectorstore and return structured match documents.

        Args:
            query:            The user question / search string.
            conversation_id:  When provided, only chunks belonging to this
                              conversation are returned (metadata filter).

        Returns:
            List of dicts with 'content', 'metadata', and 'doc_id' keys.

        """
        logger.info(
            f"[RAG RETRIEVAL] query='{query[:80]}…'  "
            f"conversation_id='{conversation_id}'  k={self.k}",
        )

        docs = persistent_vector_store.similarity_search(
            query,
            k=self.k,
            conversation_id=conversation_id,
        )

        if not docs:
            logger.warning(
                f"[RAG RETRIEVAL] Zero documents retrieved for conversation_id='{conversation_id}'. "
                "This means either no documents have been uploaded for this conversation yet, "
                "or the conversation_id was not stored in metadata during ingestion.",
            )
            return []

        results = []
        for i, doc in enumerate(docs):
            doc_id = doc.metadata.get("source", f"chunk-{i}")
            results.append(
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "doc_id": doc_id,
                },
            )

        logger.info(
            f"[RAG RETRIEVAL] Retrieved {len(results)} chunk(s). "
            f"doc_ids={[r['doc_id'] for r in results]}",
        )
        return results


document_retriever = DocumentRetriever()
