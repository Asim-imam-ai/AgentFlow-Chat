import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

class Settings:
    """
    Central configuration class for the entire project.
    All environment variables are accessed from here.
    """

    # ===== LLM CONFIG =====
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.7))

    # ===== TOOL CONFIG =====
    TAVILY_API_KEY: str | None = os.getenv("TAVILY_API_KEY")

    # ===== APP CONFIG =====
    APP_NAME: str = "AgentFlow Chat"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # ===== VALIDATION =====
    def validate(self):
        """Ensure required keys are present"""
        if not self.OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY is missing in .env")

        if not self.TAVILY_API_KEY:
            raise ValueError("❌ TAVILY_API_KEY is missing in .env")


# Create a single global settings object
settings = Settings()

# Validate at startup
settings.validate()