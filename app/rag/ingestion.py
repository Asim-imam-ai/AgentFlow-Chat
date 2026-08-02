import logging
import os

from app.rag.loaders.csv_loader import CSVLoader
from app.rag.loaders.markdown_loader import MarkdownLoader
from app.rag.loaders.pdf_loader import PDFLoader
from app.rag.loaders.text_loader import TextLoader
from app.rag.splitter import TextSplitter
from app.rag.vectorstore import persistent_vector_store

logger = logging.getLogger("agentflow.rag.ingestion")


class IngestionManager:
    def __init__(self):
        self.splitter = TextSplitter()

    def ingest_file(
        self,
        file_path: str,
        conversation_id: str | None = None,
    ) -> dict:
        """
        Load, split and embed a single document into the vector store.

        Args:
            file_path:        Absolute path to the saved file.
            conversation_id:  Thread/conversation that owns this document.
                              Stored as metadata so retrieval can filter by it.

        Returns:
            A summary dict with ingestion statistics (for logging/auditing).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        basename = os.path.basename(file_path)
        ext = os.path.splitext(basename)[1].lower()

        logger.info(
            f"[RAG INGESTION] File: '{basename}'  "
            f"ext='{ext}'  conversation_id='{conversation_id}'"
        )

        # ── 1. Select loader ──────────────────────────────────────────────
        if ext in (".txt", ".log"):
            loader = TextLoader(file_path)
        elif ext == ".md":
            loader = MarkdownLoader(file_path)
        elif ext == ".csv":
            loader = CSVLoader(file_path)
        elif ext == ".pdf":
            loader = PDFLoader(file_path)
        else:
            logger.warning(
                f"Unsupported extension '{ext}' — falling back to plain-text loader."
            )
            loader = TextLoader(file_path)

        # ── 2. Load content ───────────────────────────────────────────────
        try:
            content = loader.load()
        except Exception as e:
            logger.error(f"[RAG INGESTION] Failed to load '{basename}': {e}")
            raise

        text_length = len(content.strip())
        if text_length == 0:
            logger.warning(f"[RAG INGESTION] '{basename}' is empty — skipping.")
            return {
                "filename": basename,
                "text_length": 0,
                "chunks": 0,
                "embeddings": 0,
            }

        logger.info(
            f"[RAG INGESTION] Extracted {text_length} characters from '{basename}'."
        )

        # ── 3. Split into chunks ──────────────────────────────────────────
        chunks = self.splitter.split_text(content)
        logger.info(f"[RAG INGESTION] Split '{basename}' into {len(chunks)} chunks.")

        # ── 4. Build metadata ─────────────────────────────────────────────
        metadatas = []
        for i, _ in enumerate(chunks):
            meta = {
                "source": basename,
                "file_path": file_path,
                "chunk_index": i,
            }
            if conversation_id:
                meta["conversation_id"] = conversation_id
            metadatas.append(meta)

        # ── 5. Store in vector store ──────────────────────────────────────
        persistent_vector_store.add_texts(texts=chunks, metadatas=metadatas)
        logger.info(
            f"[RAG INGESTION] Indexed {len(chunks)} embeddings for '{basename}' "
            f"(conversation_id='{conversation_id}')."
        )

        return {
            "filename": basename,
            "text_length": text_length,
            "chunks": len(chunks),
            "embeddings": len(chunks),
            "conversation_id": conversation_id,
        }


ingestion_manager = IngestionManager()
