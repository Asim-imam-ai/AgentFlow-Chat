from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # ===== APP CONFIG =====
    APP_NAME: str = "AgentFlow Chat API"
    DEBUG: bool = True
    API_PREFIX: str = "/api"

    # ===== SECURITY =====
    SECRET_KEY: str = Field(default="supersecretagentflowkeychangeinproduction")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # ===== LLM PROVIDERS =====
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    TAVILY_API_KEY: str | None = None

    # ===== DEFAULT MODELS =====
    # Can be gpt-4o-mini, gemini-1.5-flash, etc.
    DEFAULT_LLM_PROVIDER: str = "openai"  # "openai" or "gemini"
    OPENAI_MODEL: str = "gpt-4o-mini"
    GEMINI_MODEL: str = "gemini-1.5-flash"
    TEMPERATURE: float = 0.7

    # ===== UPLOAD CONFIG =====
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB


settings = Settings()
