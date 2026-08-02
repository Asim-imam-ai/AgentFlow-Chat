from sqlalchemy.orm import Session
from app.repositories.conversation_repository import ConversationRepository
from typing import List, Optional

class ConversationService:
    def __init__(self, db: Session):
        self.repo = ConversationRepository(db)

    def list_all_conversations(self):
        return self.repo.get_all()

    def get_conversation(self, conversation_id: str):
        return self.repo.get_by_id(conversation_id)

    def create_conversation(self, conversation_id: str, provider: Optional[str] = None, temperature: Optional[float] = None):
        return self.repo.create(conversation_id, provider=provider, temperature=temperature)

    def create_or_update_summary(self, conversation_id: str, summary: str, **kwargs):
        return self.repo.create_or_update(conversation_id, summary, **kwargs)

    def delete_conversation(self, conversation_id: str) -> bool:
        return self.repo.delete(conversation_id)
