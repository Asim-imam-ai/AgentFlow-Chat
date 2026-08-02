import os
from typing import Any

import requests

# Resolve API prefix
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_PREFIX = f"{BACKEND_URL}/api"


class AgentFlowAPI:
    @staticmethod
    def get_health() -> dict[str, Any]:
        try:
            res = requests.get(f"{API_PREFIX}/health")
            res.raise_for_status()
            return res.json()
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    @staticmethod
    def create_thread() -> str | None:
        try:
            res = requests.post(f"{API_PREFIX}/thread/new")
            res.raise_for_status()
            data = res.json()
            if data.get("success") and "data" in data:
                return data["data"].get("thread_id")
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to create new thread: {e}")

    @staticmethod
    def get_conversations() -> list[dict[str, Any]]:
        try:
            res = requests.get(f"{API_PREFIX}/conversations")
            res.raise_for_status()
            return res.json().get("conversations", [])
        except Exception as e:
            raise RuntimeError(f"Failed to load conversations: {e}")

    @staticmethod
    def get_history(conversation_id: str) -> dict[str, Any]:
        try:
            res = requests.get(f"{API_PREFIX}/history/{conversation_id}")
            res.raise_for_status()
            return res.json()
        except Exception as e:
            raise RuntimeError(
                f"Failed to load history for conversation {conversation_id}: {e}",
            )

    @staticmethod
    def delete_thread(conversation_id: str) -> dict[str, Any]:
        try:
            res = requests.post(f"{API_PREFIX}/thread/{conversation_id}/clear")
            res.raise_for_status()
            return res.json()
        except Exception as e:
            raise RuntimeError(f"Failed to delete thread {conversation_id}: {e}")

    @staticmethod
    def upload_file(
        file_bytes: bytes,
        file_name: str,
        conversation_id: str | None = None,
    ) -> dict[str, Any]:
        try:
            files = {"file": (file_name, file_bytes)}
            data = {}
            if conversation_id:
                data["conversation_id"] = conversation_id
            res = requests.post(f"{API_PREFIX}/upload", files=files, data=data)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            raise RuntimeError(f"Failed to upload document: {e}")

    @staticmethod
    def send_chat(
        message: str,
        conversation_id: str,
        provider: str = "openai",
        temperature: float = 0.7,
    ) -> dict[str, Any]:
        try:
            payload = {
                "message": message,
                "conversation_id": conversation_id,
                "provider": provider,
                "temperature": temperature,
            }
            res = requests.post(f"{API_PREFIX}/chat", json=payload)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}")

    @staticmethod
    def rename_thread(conversation_id: str, summary: str) -> dict[str, Any]:
        try:
            res = requests.post(
                f"{API_PREFIX}/thread/{conversation_id}/rename",
                params={"summary": summary},
            )
            res.raise_for_status()
            return res.json()
        except Exception as e:
            raise RuntimeError(f"Failed to rename thread: {e}")
