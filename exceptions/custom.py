class AgentFlowException(Exception):
    """Base exception for all AgentFlow operations."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class IngestionException(AgentFlowException):
    """Exception raised when document loading or ingestion fails."""


class LLMException(AgentFlowException):
    """Exception raised when API calls to OpenAI or Gemini fail."""
