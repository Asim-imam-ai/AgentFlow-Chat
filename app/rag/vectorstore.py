import logging
import os
import pickle

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from app.rag.embeddings import get_embeddings

logger = logging.getLogger("agentflow.rag.vectorstore")
VECTORSTORE_PATH = os.path.join("data", "vectorstore.pkl")


class PersistentVectorStore:
    """
    Wrapper for InMemoryVectorStore with local pickle-based file persistence.
    Supports per-conversation metadata filtering so that retrieval only returns
    chunks that were indexed for the active conversation thread.
    """

    def __init__(self):
        self.embeddings = get_embeddings()
        self.vectorstore: InMemoryVectorStore = None  # type: ignore
        self.load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def load(self) -> None:
        """Load vectorstore from disk if it exists, else create a new empty store."""
        if os.path.exists(VECTORSTORE_PATH):
            try:
                with open(VECTORSTORE_PATH, "rb") as f:
                    self.vectorstore = pickle.load(f)
                # Rebind embedding function (not serialised reliably)
                self.vectorstore.embeddings = self.embeddings
                logger.info("Vectorstore loaded from disk.")
                return
            except Exception as e:
                logger.error(
                    f"Failed to load vectorstore from disk ({e}). Creating a fresh store."
                )
                # Remove corrupt file so it is not loaded again next restart
                try:
                    os.remove(VECTORSTORE_PATH)
                except OSError:
                    pass

        logger.info("Creating new empty vectorstore.")
        self.vectorstore = InMemoryVectorStore(embedding=self.embeddings)

    def save(self) -> None:
        """Persist vectorstore state to disk."""
        os.makedirs(os.path.dirname(VECTORSTORE_PATH) or ".", exist_ok=True)
        try:
            with open(VECTORSTORE_PATH, "wb") as f:
                pickle.dump(self.vectorstore, f)
            logger.info("Vectorstore saved to disk.")
        except Exception as e:
            logger.error(f"Failed to save vectorstore to disk: {e}")

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------
    def add_texts(
        self,
        texts: list[str],
        metadatas: list[dict] | None = None,
    ) -> None:
        """Embed and store texts; persist immediately."""
        docs = [
            Document(
                page_content=text,
                metadata=metadatas[i] if metadatas else {},
            )
            for i, text in enumerate(texts)
        ]
        self.vectorstore.add_documents(docs)
        self.save()
        logger.info(f"Added {len(docs)} document chunk(s) to vectorstore.")

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        conversation_id: str | None = None,
    ) -> list[Document]:
        """
        Search for chunks similar to *query*.

        If *conversation_id* is provided the results are **filtered** so that
        only chunks whose metadata ``conversation_id`` matches are returned.
        This is done via post-fetch filtering because InMemoryVectorStore does
        not guarantee a reliable ``filter=`` kwarg across all versions.

        To compensate for the post-filter reduction we fetch up to
        ``k * 10`` candidates first, then trim to *k* after filtering.
        """
        if conversation_id:
            candidates = self.vectorstore.similarity_search(query, k=k * 10)
            filtered = [
                doc
                for doc in candidates
                if doc.metadata.get("conversation_id") == conversation_id
            ]
            logger.info(
                f"Similarity search for conv '{conversation_id}': "
                f"{len(candidates)} candidates → {len(filtered)} after filter, returning top {k}."
            )
            return filtered[:k]

        results = self.vectorstore.similarity_search(query, k=k)
        logger.info(
            f"Similarity search (no conv filter): returned {len(results)} results."
        )
        return results

    def get_document_count(self, conversation_id: str | None = None) -> int:
        """Return total indexed chunks, optionally scoped to a conversation."""
        try:
            all_docs = self.vectorstore.similarity_search("", k=10_000)
        except Exception:
            return 0
        if conversation_id:
            return sum(
                1
                for d in all_docs
                if d.metadata.get("conversation_id") == conversation_id
            )
        return len(all_docs)


# Global singleton
persistent_vector_store = PersistentVectorStore()
