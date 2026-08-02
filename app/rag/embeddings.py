import logging

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.settings import settings

logger = logging.getLogger("agentflow.rag.embeddings")


def get_embeddings():
    """Returns Google Generative AI Embeddings using the gemini-embedding-001 model.
    This is the only embedding provider confirmed to work with the available API keys.
    The OpenAI project does not have access to any embedding models.
    """
    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Google Generative AI Embeddings (gemini-embedding-001) are required for RAG.",
        )

    logger.info(
        "Initializing Google Generative AI Embeddings (gemini-embedding-001)...",
    )
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.GEMINI_API_KEY,
    )
