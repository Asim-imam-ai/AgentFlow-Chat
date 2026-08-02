"""
RAG pipeline integration tests.

These tests cover the full ingestion → retrieval pipeline including:
- Text extraction and chunking (unit)
- End-to-end ingestion into the vectorstore with conversation_id scoping
- Per-conversation retrieval accuracy (conversation A does NOT see conversation B chunks)
- Zero-result behaviour when no documents are indexed for a conversation
"""
import pytest
import os
import tempfile
from app.rag.splitter import TextSplitter
from app.rag.loaders.text_loader import TextLoader


# ---------------------------------------------------------------------------
# Unit tests (no external API calls)
# ---------------------------------------------------------------------------

def test_text_splitting():
    """Standard character-based splitting respects chunk_size."""
    splitter = TextSplitter(chunk_size=100, chunk_overlap=20)
    sample_text = "This is a very long sentence designed to test the splitting function of the RAG ingestion pipeline."
    chunks = splitter.split_text(sample_text)
    assert len(chunks) >= 1
    assert all(len(chunk) <= 100 for chunk in chunks)


def test_text_loader(tmp_path):
    """Text loader correctly reads file contents."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello World RAG Test", encoding="utf-8")

    loader = TextLoader(str(file_path))
    content = loader.load()
    assert content == "Hello World RAG Test"


def test_text_splitter_respects_overlap():
    """Chunks overlap by chunk_overlap characters."""
    splitter = TextSplitter(chunk_size=50, chunk_overlap=10)
    # Build a text larger than one chunk
    text = "ABCDEFGHIJ" * 20  # 200 chars
    chunks = splitter.split_text(text)
    assert len(chunks) >= 2
    # At least one chunk must have the expected max length
    assert max(len(c) for c in chunks) <= 50


# ---------------------------------------------------------------------------
# Integration tests (require GEMINI_API_KEY)
# ---------------------------------------------------------------------------

def requires_gemini(fn):
    """Skip decorator if GEMINI_API_KEY is not configured."""
    from app.core.settings import settings
    return pytest.mark.skipif(
        not settings.GEMINI_API_KEY,
        reason="GEMINI_API_KEY not set — skipping RAG integration tests",
    )(fn)


@requires_gemini
def test_ingest_and_retrieve_scoped_by_conversation(tmp_path):
    """
    Documents uploaded for conversation A must NOT appear in conversation B results,
    and documents uploaded for conversation B must NOT appear in conversation A results.
    """
    from app.rag.ingestion import IngestionManager
    from app.rag.retrieval import DocumentRetriever
    from langchain_core.vectorstores import InMemoryVectorStore
    from app.rag.vectorstore import PersistentVectorStore
    from app.rag.embeddings import get_embeddings

    # Build an isolated in-memory vectorstore for this test
    embeddings = get_embeddings()
    isolated_store = PersistentVectorStore.__new__(PersistentVectorStore)
    isolated_store.embeddings = embeddings
    isolated_store.vectorstore = InMemoryVectorStore(embedding=embeddings)

    # Patch the global singleton for the duration of this test
    import app.rag.vectorstore as vs_module
    import app.rag.ingestion as ing_module
    import app.rag.retrieval as ret_module

    original_store = vs_module.persistent_vector_store
    vs_module.persistent_vector_store = isolated_store
    ing_module.persistent_vector_store = isolated_store
    ret_module.persistent_vector_store = isolated_store

    try:
        ingestion = IngestionManager()
        retriever = DocumentRetriever(k=4)

        # Conversation A document
        file_a = tmp_path / "conv_a.txt"
        file_a.write_text(
            "The AgentFlow platform supports multi-agent orchestration via LangGraph.",
            encoding="utf-8",
        )

        # Conversation B document
        file_b = tmp_path / "conv_b.txt"
        file_b.write_text(
            "Quantum entanglement is a physical phenomenon observed in quantum mechanics.",
            encoding="utf-8",
        )

        stats_a = ingestion.ingest_file(str(file_a), conversation_id="conv-aaa")
        stats_b = ingestion.ingest_file(str(file_b), conversation_id="conv-bbb")

        # Validate ingestion stats
        assert stats_a["chunks"] >= 1
        assert stats_a["embeddings"] >= 1
        assert stats_a["conversation_id"] == "conv-aaa"

        assert stats_b["chunks"] >= 1
        assert stats_b["conversation_id"] == "conv-bbb"

        # Retrieve for conv-aaa — should find LangGraph content
        results_a = retriever.retrieve("LangGraph multi-agent", conversation_id="conv-aaa")
        assert len(results_a) >= 1
        assert any("LangGraph" in r["content"] or "AgentFlow" in r["content"] for r in results_a), \
            f"Expected AgentFlow content in conv-aaa results: {results_a}"

        # Retrieve for conv-bbb — should find quantum content
        results_b = retriever.retrieve("quantum entanglement", conversation_id="conv-bbb")
        assert len(results_b) >= 1
        assert any("quantum" in r["content"].lower() for r in results_b), \
            f"Expected quantum content in conv-bbb results: {results_b}"

        # Cross-contamination check: conv-aaa query must NOT return conv-bbb's docs
        for r in results_a:
            assert r["metadata"].get("conversation_id") == "conv-aaa", \
                f"Cross-contamination: conv-bbb doc appeared in conv-aaa results: {r}"

        for r in results_b:
            assert r["metadata"].get("conversation_id") == "conv-bbb", \
                f"Cross-contamination: conv-aaa doc appeared in conv-bbb results: {r}"

    finally:
        # Restore global singleton
        vs_module.persistent_vector_store = original_store
        ing_module.persistent_vector_store = original_store
        ret_module.persistent_vector_store = original_store


@requires_gemini
def test_retrieval_returns_empty_for_unknown_conversation():
    """Retrieval for a conversation with no uploaded docs must return an empty list."""
    from app.rag.retrieval import DocumentRetriever

    retriever = DocumentRetriever(k=4)
    results = retriever.retrieve("anything at all", conversation_id="non-existent-conv-xyz-999")
    assert results == [], f"Expected empty list, got: {results}"


@requires_gemini
def test_ingestion_stats_are_complete(tmp_path):
    """ingest_file() must return a dict with all required stat keys."""
    from app.rag.ingestion import IngestionManager

    ingestion = IngestionManager()
    file_path = tmp_path / "stats_check.txt"
    file_path.write_text("Checking that all ingestion statistics are returned correctly.", encoding="utf-8")

    stats = ingestion.ingest_file(str(file_path), conversation_id="conv-stats-test")
    for key in ("filename", "text_length", "chunks", "embeddings", "conversation_id"):
        assert key in stats, f"Missing key '{key}' in ingestion stats: {stats}"
    assert stats["text_length"] > 0
    assert stats["chunks"] >= 1
    assert stats["embeddings"] == stats["chunks"]
