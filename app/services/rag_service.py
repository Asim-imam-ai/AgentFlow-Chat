import logging
from typing import Any

from app.rag.ingestion import ingestion_manager
from app.rag.retrieval import document_retriever

logger = logging.getLogger("agentflow.services.rag_service")


class RAGServiceWrapper:
    """Thin facade that exposes RAG utilities to the rest of the FastAPI service layer.
    All operations are conversation-scoped via the conversation_id parameter.
    """

    def ingest_document(
        self,
        file_path: str,
        conversation_id: str | None = None,
    ) -> dict:
        """Ingest a file into the vectorstore, tagged with the conversation_id.

        Returns a stats dict: {filename, text_length, chunks, embeddings, conversation_id}.
        """
        return ingestion_manager.ingest_file(
            file_path=file_path,
            conversation_id=conversation_id,
        )

    def search_documents(
        self,
        query: str,
        conversation_id: str | None = None,
        limit: int = 4,
    ) -> list[dict[str, Any]]:
        """Retrieve matching document snippets scoped to conversation_id.
        Returns an empty list when no matching documents are found.
        """
        document_retriever.k = limit
        return document_retriever.retrieve(
            query=query,
            conversation_id=conversation_id,
        )


rag_service_wrapper = RAGServiceWrapper()
