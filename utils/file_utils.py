import os
import re


def get_file_extension(filename: str) -> str:
    """Return lowercase file extension, e.g. '.pdf'"""
    return os.path.splitext(filename)[1].lower()


def is_safe_filename(filename: str) -> bool:
    """Check if filename does not contain path traversal characters"""
    return not (".." in filename or "/" in filename or "\\" in filename)


def clean_filename(filename: str) -> str:
    """Sanitize filename to prevent security injection issues"""
    # Remove any character that is not alphanumeric, dot, hyphen or underscore
    return re.sub(r"[^a-zA-Z0-9.\-_]", "_", filename)


def get_file_size_mb(filepath: str) -> float:
    """Return size of file in megabytes"""
    if os.path.exists(filepath):
        return os.path.getsize(filepath) / (1024 * 1024)
    return 0.0
