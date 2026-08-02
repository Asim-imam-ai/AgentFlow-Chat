from sqlalchemy.orm import Session
from app.database.models import MemoryModel
from typing import Dict, Optional

class MemoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_value(self, key: str) -> Optional[str]:
        mem = self.db.query(MemoryModel).filter(MemoryModel.key == key).first()
        return mem.value if mem else None

    def get_all(self) -> Dict[str, str]:
        memories = self.db.query(MemoryModel).all()
        return {mem.key: mem.value for mem in memories}

    def set_value(self, key: str, value: str) -> MemoryModel:
        mem = self.db.query(MemoryModel).filter(MemoryModel.key == key).first()
        if mem:
            mem.value = value
        else:
            mem = MemoryModel(key=key, value=value)
            self.db.add(mem)
        self.db.commit()
        self.db.refresh(mem)
        return mem

    def delete_key(self, key: str) -> bool:
        mem = self.db.query(MemoryModel).filter(MemoryModel.key == key).first()
        if mem:
            self.db.delete(mem)
            self.db.commit()
            return True
        return False
