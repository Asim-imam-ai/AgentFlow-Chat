import os

class TextLoader:
    """
    Simple loader for plain text files.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> str:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
            
        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
