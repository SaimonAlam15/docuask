from app.documents.embeddings.openai import OpenAIEmbeddingProvider

embedder = OpenAIEmbeddingProvider(
    api_key="",
    embedding_model="text-embedding-3-small",
)


async def get_embedding():
    """Fetch and print embeddings for a sample text."""
    embeddings = await embedder.embed(
        ["Did Saimon Alam work for a company in New York, USA (Remote)"]
    )
    print(embeddings)


if __name__ == "__main__":
    import asyncio

    asyncio.run(get_embedding())
