from typing import Protocol


class DocumentChunker(Protocol):
    def chunk(self, text: str) -> list[str]:
        pass
