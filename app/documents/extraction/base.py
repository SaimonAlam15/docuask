from pathlib import Path
from typing import Protocol


class DocumentExtractor(Protocol):
    def extract_text(self, file_path: Path) -> str:
        pass
