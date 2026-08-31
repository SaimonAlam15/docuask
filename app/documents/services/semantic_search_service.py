import logging

from app.documents.embeddings.base import EmbeddingProvider
from app.documents.repositories.document_chunk_repository import DocumentChunkRepository

logger = logging.getLogger(__name__)


class SemanticSearchService:
    def __init__(
        self,
        chunk_repo: DocumentChunkRepository,
        embedding_provider: EmbeddingProvider,
        user_id: str = None,
    ):
        self.chunk_repo = chunk_repo
        self.embedding_provider = embedding_provider
        self.user_id = user_id

    async def embed_and_search(self, query: str):
        query_embedding = await self.embedding_provider.embed([query])
        if not query_embedding:
            logger.error("Unable to embed query")
            raise RuntimeError("Unable to generate embedding for search query")

        # TODO: get user from request
        search_result = await self.chunk_repo.find_similar_chunks(
            query_embedding=query_embedding[0], user_id="77b03295-6eab-4d37-9429-2eeef614f278"
        )
        return search_result
