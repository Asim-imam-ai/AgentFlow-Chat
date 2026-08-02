from sqlalchemy.orm import Session
from app.repositories.memory_repository import MemoryRepository
from typing import Dict, Optional

class MemoryService:
    def __init__(self, db: Session):
        self.repo = MemoryRepository(db)

    def get_fact(self, key: str) -> Optional[str]:
        return self.repo.get_value(key)

    def get_all_facts(self) -> Dict[str, str]:
        return self.repo.get_all()

    def set_fact(self, key: str, value: str):
        return self.repo.set_value(key, value)

    def delete_fact(self, key: str) -> bool:
        return self.repo.delete_key(key)
