import os

# Backend API base URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_PREFIX = f"{BACKEND_URL}/api"
