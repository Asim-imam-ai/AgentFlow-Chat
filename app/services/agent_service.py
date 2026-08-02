import logging
import uuid

from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy.orm import Session

from app.graph.factory import get_graph
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService

logger = logging.getLogger("agentflow.services.agent_service")


class AgentService:
    def __init__(self, db: Session):
        self.chat_service = ChatService(db)
        self.conversation_service = ConversationService(db)

    def execute_agent_turn(
        self,
        message: str,
        conversation_id: str | None = None,
        provider: str | None = None,
        model_name: str | None = None,
        temperature: float | None = None,
    ) -> dict:
        """Execute one full conversation turn.
        Invokes the LangGraph compiled state graph, saves history and updates SQL DB.
        """
        active_id = conversation_id or str(uuid.uuid4())
        logger.info(f"Running agent turn for conversation {active_id}")

        graph = get_graph()
        config = {"configurable": {"thread_id": active_id}}

        # 1. Save user message to SQL DB
        self.chat_service.save_message(active_id, "user", message)

        # 2. Prepare graph inputs
        user_msg = HumanMessage(content=message)
        inputs = {
            "messages": [user_msg],
            "conversation_id": active_id,  # Needed by the RAG node for per-thread retrieval
        }
        if provider:
            inputs["provider"] = provider
        if model_name:
            inputs["model_name"] = model_name
        if temperature is not None:
            inputs["temperature"] = temperature

        # 3. Invoke graph
        output_state = graph.invoke(inputs, config)

        # 4. Extract assistant response & summary
        messages = output_state.get("messages", [])
        summary = output_state.get("summary", "")

        assistant_resp = "Sorry, I couldn't process that request."
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                assistant_resp = msg.content
                break

        # 5. Save assistant reply to SQL DB
        self.chat_service.save_message(active_id, "assistant", assistant_resp)

        # 6. Update conversation summary in SQL DB
        kwargs = {}
        if provider:
            kwargs["provider"] = provider
        if temperature is not None:
            kwargs["temperature"] = temperature

        self.conversation_service.create_or_update_summary(
            active_id,
            summary or "",
            **kwargs,
        )

        return {
            "response": assistant_resp,
            "conversation_id": active_id,
            "summary": summary or None,
        }


# We do not define a global instance because it needs a DB Session parameter
