from app.rag.ingestion import ingestion_manager
from app.rag.retrieval import document_retriever
from typing import List, Dict, Any
import logging

logger = logging.getLogger("agentflow.rag.service")

class RAGService:
    def ingest_document(self, file_path: str) -> None:
        """Ingest a file into vectorstore."""
        ingestion_manager.ingest_file(file_path)

    def retrieve_context(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Retrieve matching document snippets."""
        document_retriever.k = limit
        return document_retriever.retrieve(query)

rag_service = RAGService()
