from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class OpenAILLMProvider:
    def __init__(self, api_key: str, model: str):
        self.__api_key = api_key
        self.__client = AsyncOpenAI(api_key=self.__api_key)
        self.__model = model

    async def generate(self, prompt: str, response_model=type[T]) -> T:
        response = await self.__client.beta.chat.completions.parse(
            model=self.__model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            response_format=response_model,
        )
        return response.choices[0].message.parsed
