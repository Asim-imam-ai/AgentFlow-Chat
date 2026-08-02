import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/chatbot_memory.db")

# For sqlite: check_same_thread=False is required for multi-threaded FastAPI apps
if DATABASE_URL.startswith("sqlite"):
    # Ensure directory exists
    os.makedirs("./data", exist_ok=True)
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency generator for DB sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
