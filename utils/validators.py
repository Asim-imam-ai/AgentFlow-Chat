import re


def validate_email(email: str) -> bool:
    """Validate standard email structure."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_uuid(val: str) -> bool:
    """Validate string matches UUIDv4 format."""
    pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    return bool(re.match(pattern, val.lower()))


def validate_model_provider(
    provider: str, allowed_providers: list[str] = ["openai", "gemini"]
) -> bool:
    """Check if model provider is allowed."""
    return provider.lower() in allowed_providers
