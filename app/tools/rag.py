import logging
import os

from langchain_core.tools import tool

from app.core.settings import settings
from app.tools.registry import tool_registry

logger = logging.getLogger("agentflow.tools.rag")


@tool("document_retriever")
def rag_tool(query: str) -> str:
    """Search and retrieve context from uploaded documents.
    Use this when the user asks questions about their uploaded files or documents.
    """
    upload_dir = settings.UPLOAD_DIR
    if not os.path.exists(upload_dir):
        return f"Document directory '{upload_dir}' does not exist. No documents have been uploaded yet."

    files = [f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))]
    if not files:
        return "No documents found in the upload directory. Please upload documents first."

    query_terms = query.lower().split()
    results = []

    for filename in files:
        file_path = os.path.join(upload_dir, filename)
        # We handle text files for simplicity.
        # In production, we'd use PDF/Docx loaders + Vector DB.
        if filename.endswith(".txt") or filename.endswith(".md"):
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                paragraphs = content.split("\n\n")
                for para in paragraphs:
                    para_clean = para.strip()
                    if not para_clean:
                        continue
                    # Score paragraph based on term match count
                    score = sum(1 for term in query_terms if term in para_clean.lower())
                    if score > 0:
                        results.append((score, filename, para_clean[:500]))
            except Exception as e:
                logger.error(f"Error reading file {filename}: {e}")

    if not results:
        return f"No matches found for search query: '{query}' in uploaded documents."

    # Sort by score descending
    results.sort(key=lambda x: x[0], reverse=True)

    # Format top 3 results
    top_results = results[:3]
    formatted = []
    for score, filename, chunk in top_results:
        formatted.append(f"Source: {filename}\nContent snippet: {chunk}\n")

    return "\n---\n".join(formatted)


# Register tool
tool_registry.register(rag_tool)
