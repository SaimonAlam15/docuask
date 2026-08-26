from typing import Protocol


class EmbeddingProvider(Protocol):
    async def embed(self, text: list[str]) -> list[list[float]]:
        pass
