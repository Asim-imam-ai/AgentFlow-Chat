import logging

logger = logging.getLogger("agentflow.utils.model_utils")


def estimate_token_count(text: str) -> int:
    """Rough estimation of token count for text.
    In production, use tiktoken or model specific tokenizers.
    """
    if not text:
        return 0
    # Rule of thumb: 1 token is ~4 characters or ~0.75 words.
    # Let's count words and multiply by 1.3
    words = text.split()
    return int(len(words) * 1.3)


def get_pricing_estimate(
    tokens: int,
    model_name: str,
    direction: str = "input",
) -> float:
    """Return rough USD pricing for model usage."""
    model_lower = model_name.lower()
    # Simple lookup rates per 1M tokens
    pricing_rates = {
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-4o-mini": {"input": 0.150, "output": 0.600},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.300},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    }

    # Match rate
    rate = 0.0
    for name, rates in pricing_rates.items():
        if name in model_lower:
            rate = rates.get(direction, 0.0)
            break

    return (tokens / 1_000_000) * rate
