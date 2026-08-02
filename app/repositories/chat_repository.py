from sqlalchemy.orm import Session
from app.database.models import MessageModel, ConversationModel
from typing import List
import datetime

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_message(self, conversation_id: str, role: str, content: str) -> MessageModel:
        # Ensure conversation exists
        conv = self.db.query(ConversationModel).filter(ConversationModel.conversation_id == conversation_id).first()
        if not conv:
            conv = ConversationModel(
                conversation_id=conversation_id,
                summary="",
                message_count=0,
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow()
            )
            self.db.add(conv)
            self.db.commit()

        msg = MessageModel(conversation_id=conversation_id, role=role, content=content)
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)

        # Update conversation stats
        msg_count = self.db.query(MessageModel).filter(MessageModel.conversation_id == conversation_id).count()
        conv.message_count = msg_count
        conv.last_message = content
        conv.updated_at = datetime.datetime.utcnow()
        self.db.commit()

        return msg

    def get_messages_by_conversation(self, conversation_id: str) -> List[MessageModel]:
        return self.db.query(MessageModel).filter(MessageModel.conversation_id == conversation_id).order_by(MessageModel.created_at.asc()).all()

    def clear_history(self, conversation_id: str) -> None:
        self.db.query(MessageModel).filter(MessageModel.conversation_id == conversation_id).delete()
        self.db.commit()
