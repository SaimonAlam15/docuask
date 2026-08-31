from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.models.document_chunk import DocumentChunk
from app.documents.schemas.document_chunk import DocumentChunkCreate


class DocumentChunkRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_document_chunks(
        self, chunks: list[DocumentChunkCreate]
    ) -> list[DocumentChunk]:
        db_chunks = [
            DocumentChunk(
                document_content_id=chunk.document_content_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                embedding=chunk.embedding,
            )
            for chunk in chunks
        ]
        self.__db.add_all(db_chunks)
        await self.__db.flush()
        return db_chunks

    async def find_similar_chunks(
        self, query_embedding: list[float], limit: int = 5
    ) -> list[tuple[DocumentChunk, float]]:
        distance_expr = DocumentChunk.embedding.cosine_distance(query_embedding)

        stmt = select(DocumentChunk, distance_expr).order_by(distance_expr.asc()).limit(limit)

        result = await self.__db.execute(stmt)
        return result.all()
