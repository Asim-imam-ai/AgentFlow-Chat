import logging
from typing import Any

from app.rag.ingestion import ingestion_manager
from app.rag.retrieval import document_retriever

logger = logging.getLogger("agentflow.rag.service")


class RAGService:
    def ingest_document(self, file_path: str) -> None:
        """Ingest a file into vectorstore."""
        ingestion_manager.ingest_file(file_path)

    def retrieve_context(self, query: str, limit: int = 3) -> list[dict[str, Any]]:
        """Retrieve matching document snippets."""
        document_retriever.k = limit
        return document_retriever.retrieve(query)


rag_service = RAGService()
