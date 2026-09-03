from typing import Protocol

from app.llm.schemas.answer import LLMResponse


class LLMProvider(Protocol):
    async def generate(self, prompt: str) -> LLMResponse:
        pass
