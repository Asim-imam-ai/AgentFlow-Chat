import os
import sys

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

from app.database.models import ConversationModel, MemoryModel
from app.database.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agentflow.scripts.seed")


def seed():
    logger.info("Seeding database values...")
    db = SessionLocal()
    try:
        # 1. Seed some standard memories
        memories = [
            ("user_name", "Developer"),
            ("coding_preferences", "Python, FastAPI, and LangGraph"),
            ("system_rules", "Answer clear and concisely with details."),
        ]

        for k, v in memories:
            existing = db.query(MemoryModel).filter(MemoryModel.key == k).first()
            if not existing:
                mem = MemoryModel(key=k, value=v)
                db.add(mem)
                logger.info(f"Seeded memory key '{k}'")

        # 2. Seed a welcome conversation if empty
        existing_conv = db.query(ConversationModel).first()
        if not existing_conv:
            welcome_conv = ConversationModel(
                id="welcome-thread-id-001",
                summary="Initial greeting and system overview.",
            )
            db.add(welcome_conv)
            logger.info("Seeded welcome conversation thread.")

        db.commit()
        logger.info("Database seeding completed.")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to seed database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
