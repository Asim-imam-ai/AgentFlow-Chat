from sqlalchemy.orm import Session
from app.database.models import ConversationModel
from typing import List, Optional
import datetime

class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, conversation_id: str) -> Optional[ConversationModel]:
        return self.db.query(ConversationModel).filter(ConversationModel.conversation_id == conversation_id).first()

    def get_all(self) -> List[ConversationModel]:
        return self.db.query(ConversationModel).order_by(ConversationModel.updated_at.desc()).all()

    def create(self, conversation_id: str, summary: Optional[str] = None, provider: Optional[str] = None, temperature: Optional[float] = None) -> ConversationModel:
        conv = ConversationModel(
            conversation_id=conversation_id,
            summary=summary or "",
            message_count=0,
            last_message=None,
            provider=provider,
            temperature=temperature,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv

    def create_or_update(self, conversation_id: str, summary: Optional[str] = None, **kwargs) -> ConversationModel:
        conv = self.get_by_id(conversation_id)
        if not conv:
            conv = ConversationModel(
                conversation_id=conversation_id,
                summary=summary or "",
                message_count=0,
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow()
            )
            self.db.add(conv)
        else:
            if summary is not None:
                conv.summary = summary

        for k, v in kwargs.items():
            if hasattr(conv, k):
                setattr(conv, k, v)

        conv.updated_at = datetime.datetime.utcnow()
        self.db.commit()
        self.db.refresh(conv)
        return conv

    def delete(self, conversation_id: str) -> bool:
        conv = self.get_by_id(conversation_id)
        if conv:
            self.db.delete(conv)
            self.db.commit()
            return True
        return False
