# import sys
# import os

# # Ensure virtual environment site-packages are loaded first to prevent path pollution
# venv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".venv", "Lib", "site-packages"))
# if os.path.exists(venv_path) and venv_path not in sys.path:
#     sys.path.insert(0, venv_path)

# import uvicorn

# def main():
#     print("Starting AgentFlow Chat FastAPI backend...")
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


# if __name__ == "__main__":
#     main()


"""
Local development entry point.

Usage:
    python main.py

Docker should NOT use this file.
Docker starts the application with:

    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn


def configure_environment() -> None:
    """
    Ensure the project's virtual environment site-packages
    are available when running locally.
    """

    project_root = Path(__file__).resolve().parent

    # Windows virtual environment
    windows_site_packages = project_root / ".venv" / "Lib" / "site-packages"

    # Linux/macOS virtual environment
    linux_site_packages = (
        project_root
        / ".venv"
        / "lib"
        / f"python{sys.version_info.major}.{sys.version_info.minor}"
        / "site-packages"
    )

    for path in (windows_site_packages, linux_site_packages):
        if path.exists():
            sys.path.insert(0, str(path))
            break


def main() -> None:
    """
    Start the FastAPI application.
    """

    configure_environment()

    print("=" * 60)
    print("🚀 Starting AgentFlow Chat Backend")
    print("Environment :", os.getenv("ENVIRONMENT", "development"))
    print("URL         : http://127.0.0.1:8000")
    print("Docs        : http://127.0.0.1:8000/docs")
    print("=" * 60)

    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
