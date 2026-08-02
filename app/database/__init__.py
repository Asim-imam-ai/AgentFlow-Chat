import logging

from sqlalchemy import inspect

from app.database.models import ConversationModel, MemoryModel, MessageModel
from app.database.session import Base, SessionLocal, engine, get_db

logger = logging.getLogger("agentflow.database")

__all__ = [
    "Base",
    "ConversationModel",
    "MemoryModel",
    "MessageModel",
    "SessionLocal",
    "engine",
    "get_db",
]

# Automated schema verification and migration helper
try:
    inspector = inspect(engine)
    if "conversations" in inspector.get_table_names():
        columns = [c["name"] for c in inspector.get_columns("conversations")]
        if "message_count" not in columns or "conversation_id" not in columns:
            logger.info(
                "Database schema is outdated (missing 'message_count' or 'conversation_id'). Dropping and recreating tables...",
            )
            Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error(f"Failed to initialize database schema: {e}")
