from sqlalchemy.orm import Session

from app.repositories.chat_repository import ChatRepository


class ChatService:
    def __init__(self, db: Session):
        self.repo = ChatRepository(db)

    def save_message(self, conversation_id: str, role: str, content: str):
        return self.repo.add_message(conversation_id, role, content)

    def get_chat_history(self, conversation_id: str):
        return self.repo.get_messages_by_conversation(conversation_id)

    def delete_chat_history(self, conversation_id: str):
        self.repo.clear_history(conversation_id)
