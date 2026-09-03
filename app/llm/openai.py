from openai import AsyncOpenAI

from app.llm.schemas.answer import LLMResponse


class OpenAILLMProvider:
    def __init__(self, api_key: str, model: str):
        self.__api_key = api_key
        self.__client = AsyncOpenAI(api_key=self.__api_key)
        self.__model = model

    async def generate(self, prompt: str) -> LLMResponse:
        response = await self.__client.beta.chat.completions.parse(
            model=self.__model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            response_format=LLMResponse,
        )
        return response.choices[0].message.parsed
