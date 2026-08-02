from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Verify health endpoint returns success code and online status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["status"] == "online"


def test_conversations_endpoint():
    """Verify list conversations returns a valid schema layout."""
    response = client.get("/api/conversations")
    assert response.status_code == 200
    json_data = response.json()
    assert "conversations" in json_data


def test_thread_and_chat_lifecycle():
    """Verify the end-to-end database-backed conversation API lifecycle."""
    # 1. Create a new thread (Fast, DB-only)
    resp = client.post("/api/thread/new")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    thread_id = data["data"]["thread_id"]
    assert thread_id is not None

    # 2. Check that the new conversation is listed with 0 messages
    resp = client.get("/api/conversations")
    assert resp.status_code == 200
    conversations = resp.json()["conversations"]
    matching = [c for c in conversations if c["conversation_id"] == thread_id]
    assert len(matching) == 1
    assert matching[0]["message_count"] == 0

    # 3. Submit a chat message (Slow, invokes LLM/graph)
    # Use a dummy test case - note that LLM calls are mocked or run locally depending on settings,
    # but here we can just verify the route responds and stores messages.
    chat_payload = {
        "message": "Verify SQLite persistence of this message.",
        "conversation_id": thread_id,
        "provider": "openai",
        "temperature": 0.5,
    }
    # We invoke it (if API key is missing or mock is not active, this might fail, but let's see.
    # Actually, test_agent.py ran, so OpenAI key is either set or mocked. Let's see if we can do this turn.)
    resp = client.post("/api/chat", json=chat_payload)
    assert resp.status_code == 200
    chat_data = resp.json()
    assert chat_data["conversation_id"] == thread_id
    assert chat_data["response"] is not None

    # 4. Check listing metadata again: should now have messages
    resp = client.get("/api/conversations")
    assert resp.status_code == 200
    conversations = resp.json()["conversations"]
    matching = [c for c in conversations if c["conversation_id"] == thread_id]
    assert len(matching) == 1
    # 1 user message + 1 assistant message = 2 messages total
    assert matching[0]["message_count"] == 2

    # 5. Get conversation history directly from SQLite (Fast, DB-only)
    resp = client.get(f"/api/history/{thread_id}")
    assert resp.status_code == 200
    history = resp.json()
    assert history["conversation_id"] == thread_id
    assert len(history["messages"]) == 2
    assert history["messages"][0]["role"] == "user"
    assert history["messages"][1]["role"] == "assistant"

    # 6. Delete/clear thread from DB (Fast, DB-only)
    resp = client.post(f"/api/thread/{thread_id}/clear")
    assert resp.status_code == 200
    assert resp.json()["success"] is True

    # 7. Verify the thread is no longer listed in conversations
    resp = client.get("/api/conversations")
    assert resp.status_code == 200
    conversations = resp.json()["conversations"]
    matching = [c for c in conversations if c["conversation_id"] == thread_id]
    assert len(matching) == 0
