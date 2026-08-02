import logging

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.settings import settings

logger = logging.getLogger("agentflow.llms.gemini")


def get_gemini_llm(model_name: str | None = None, temperature: float | None = None):
    """Get a configured ChatGoogleGenerativeAI model instance."""
    selected_model = model_name or settings.GEMINI_MODEL
    selected_temp = temperature if temperature is not None else settings.TEMPERATURE

    if not settings.GEMINI_API_KEY:
        logger.warning(
            "⚠️ GEMINI_API_KEY not found in settings. Make sure it is set in environment.",
        )

    logger.info(f"Creating Gemini LLM instance using model {selected_model}")

    return ChatGoogleGenerativeAI(
        model=selected_model,
        temperature=selected_temp,
        google_api_key=settings.GEMINI_API_KEY,
    )
