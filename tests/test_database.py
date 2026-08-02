from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.repositories.conversation_repository import ConversationRepository


def test_database_persistence():
    """Test conversation repository using in-memory isolated database engine."""
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        repo = ConversationRepository(db)

        # Test creation
        conv = repo.create_or_update(
            conversation_id="test-session", summary="First summary"
        )
        assert conv.id == "test-session"
        assert conv.summary == "First summary"

        # Test reading
        fetched = repo.get_by_id("test-session")
        assert fetched is not None
        assert fetched.summary == "First summary"

        # Test deleting
        deleted = repo.delete("test-session")
        assert deleted is True
        assert repo.get_by_id("test-session") is None
    finally:
        db.close()
