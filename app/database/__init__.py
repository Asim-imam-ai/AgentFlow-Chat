from app.database.session import Base, engine, get_db, SessionLocal
from app.database.models import ConversationModel, MessageModel, MemoryModel
from sqlalchemy import inspect
import logging

logger = logging.getLogger("agentflow.database")

__all__ = [
    "Base",
    "engine",
    "get_db",
    "SessionLocal",
    "ConversationModel",
    "MessageModel",
    "MemoryModel"
]

# Automated schema verification and migration helper
try:
    inspector = inspect(engine)
    if "conversations" in inspector.get_table_names():
        columns = [c["name"] for c in inspector.get_columns("conversations")]
        if "message_count" not in columns or "conversation_id" not in columns:
            logger.info("Database schema is outdated (missing 'message_count' or 'conversation_id'). Dropping and recreating tables...")
            Base.metadata.drop_all(bind=engine)
            
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error(f"Failed to initialize database schema: {e}")
