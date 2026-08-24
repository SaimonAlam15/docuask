import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.models.document_chunk import DocumentChunk
from app.documents.schemas.document_chunk import DocumentChunkCreate

logger = logging.getLogger(__name__)


class DocumentChunkRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_document_chunk(self, chunks: list[DocumentChunkCreate]):
        for chunk in chunks:
            try:
                db_document_chunk = DocumentChunk(
                    document_content_id=chunk.document_content_id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                )
                self.__db.add(db_document_chunk)
                await self.__db.flush()
                await self.__db.refresh(db_document_chunk)
            except Exception as e:
                logger.error("Failed to create DocumentChunk. Error: %s", str(e))
                raise
        return None
