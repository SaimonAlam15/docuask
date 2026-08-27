from openai import AsyncOpenAI


class OpenAIEmbeddingProvider:
    def __init__(self, api_key: str, embedding_model: str):
        self.__api_key = api_key
        self.__embedding_model = embedding_model
        self.__client = AsyncOpenAI(api_key=self.__api_key)

    async def embed(self, texts: list[str]) -> list[float]:
        response = await self.__client.embeddings.create(
            model=self.__embedding_model,
            input=texts,
        )

        # Extract the float array vector
        embedding_vectors = [item.embedding for item in response.data]
        return embedding_vectors
