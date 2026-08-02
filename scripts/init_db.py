import os
import sys

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

from app.database.session import Base, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agentflow.scripts.init_db")


def init_db():
    logger.info("Initializing AgentFlow database models...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully at: data/chatbot_memory.db")


if __name__ == "__main__":
    init_db()
