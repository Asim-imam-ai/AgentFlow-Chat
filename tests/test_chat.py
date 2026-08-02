from app.api.schemas.chat import ChatRequest, ChatResponse


def test_chat_schemas():
    """Test Chat schemas serialize/deserialize correctly."""
    req = ChatRequest(message="Hello", provider="openai", temperature=0.5)
    assert req.message == "Hello"
    assert req.provider == "openai"
    assert req.temperature == 0.5

    resp = ChatResponse(
        response="Hi there!",
        conversation_id="test-session-id",
        summary="A greeting session.",
    )
    assert resp.response == "Hi there!"
    assert resp.conversation_id == "test-session-id"
    assert resp.summary == "A greeting session."
