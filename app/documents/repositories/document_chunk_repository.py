from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.models.document import Document
from app.documents.models.document_chunk import DocumentChunk
from app.documents.models.document_content import DocumentContent
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
        self, query_embedding: list[float], limit: int = 5, user_id: UUID = None
    ) -> list[tuple[DocumentChunk, float]]:
        distance_expr = DocumentChunk.embedding.cosine_distance(query_embedding)

        stmt = (
            select(DocumentChunk, distance_expr)
            .join(DocumentContent, DocumentContent.id == DocumentChunk.document_content_id)
            .join(Document, Document.id == DocumentContent.document_id)
            .where(Document.user_id.is_not(None))
        )

        if user_id:
            stmt = stmt.where(Document.user_id == UUID(user_id))

        stmt = stmt.order_by(distance_expr.asc()).limit(limit)

        result = await self.__db.execute(stmt)
        return result.all()
