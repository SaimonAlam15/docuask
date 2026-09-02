from openai import AsyncOpenAI


class OpenAILLMProvider:
    def __init__(self, api_key: str, model: str):
        self.__api_key = api_key
        self.__client = AsyncOpenAI(api_key=self.__api_key)
        self.__model = model

    async def generate(self, prompt: str) -> str:
        response = await self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
