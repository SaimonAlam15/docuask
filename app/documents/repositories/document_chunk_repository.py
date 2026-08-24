import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.models.document_chunk import DocumentChunk
from app.documents.schemas.document_chunk import DocumentChunkCreate

logger = logging.getLogger(__name__)


class DocumentChunkRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_document_chunks(
        self, chunks: list[DocumentChunkCreate]
    ) -> list[DocumentChunk]:
        db_chunks = []
        try:
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
        except Exception as e:
            logger.error("Failed to create DocumentChunk. Error: %s", str(e))
            raise
        return db_chunks
