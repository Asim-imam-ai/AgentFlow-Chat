from langchain_openai import ChatOpenAI
from src.config.settings import settings


def get_llm():
    llm = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
    )
    return llm