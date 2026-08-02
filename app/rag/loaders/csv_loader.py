import csv
import os


class CSVLoader:
    """Simple loader for CSV files.
    Formats each row into a text description.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> str:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        lines = []
        with open(self.file_path, encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_str = ", ".join([f"{k}: {v}" for k, v in row.items() if v])
                lines.append(row_str)

        return "\n".join(lines)
