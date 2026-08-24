from openai import OpenAI


class OpenAIEmbeddingProvider:
    def __init__(self, api_key: str):
        self.__api_key = api_key

    async def embed(self, text: str) -> list[float]:
        client = OpenAI(api_key=self.__api_key)

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        # Extract the float array vector
        embedding_vector = response.data[0].embedding
        return embedding_vector
