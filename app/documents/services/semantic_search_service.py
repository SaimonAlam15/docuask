import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.embeddings.base import EmbeddingProvider
from app.documents.repositories.document_chunk_repository import DocumentChunkRepository

logger = logging.getLogger(__name__)


class SemanticSearchService:
    def __init__(
        self,
        session: AsyncSession,
        chunk_repo: DocumentChunkRepository,
        embedding_provider: EmbeddingProvider,
    ):
        self.session = session
        self.chunk_repo = chunk_repo
        self.embedding_provider = embedding_provider

    async def embed_and_search(self, input: str):
        input_embedding = await self.embedding_provider.embed([input])
        if len(input_embedding) == 0:
            logger.error("Unable to embed input")
            return

        search_result = await self.chunk_repo.find_similar_chunks(input_embedding[0])
        print("Result:", search_result)
        return search_result
