import logging
from uuid import UUID

from app.documents.embeddings.base import EmbeddingProvider
from app.documents.repositories.document_chunk_repository import DocumentChunkRepository

logger = logging.getLogger(__name__)


from app.documents.services.reranker import Reranker


class SemanticSearchService:
    def __init__(
        self,
        chunk_repo: DocumentChunkRepository,
        embedding_provider: EmbeddingProvider,
        reranker: Reranker,
        user_id: UUID | None = None,
    ):
        self.chunk_repo = chunk_repo
        self.embedding_provider = embedding_provider
        self.reranker = reranker
        self.user_id = user_id

    async def embed_and_search(self, query: str):
        query_embedding = await self.embedding_provider.embed([query])
        if not query_embedding:
            logger.error("Unable to embed query")
            raise RuntimeError("Unable to generate embedding for search query")

        search_result = await self.chunk_repo.find_similar_chunks(
            query_embedding=query_embedding[0],
            user_id=UUID("77b03295-6eab-4d37-9429-2eeef614f278"),
        )

        return self.reranker.rerank(
            query=query,
            results=search_result,
            top_k=10,
        )
        # return search_result
