from datetime import datetime, timezone
from typing import Dict, Any

def get_utc_timestamp() -> str:
    """Return standard ISO UTC timestamp string"""
    return datetime.now(timezone.utc).isoformat()

def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dictionaries"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

def clean_whitespace(text: str) -> str:
    """Standardize spacing and strip text."""
    if not text:
        return ""
    return " ".join(text.split())
