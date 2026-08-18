import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.models.document_file import DocumentFile
from app.documents.schemas.document_file import DocumentFileCreate

logger = logging.getLogger(__name__)


class DocumentFileRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_document_file(self, document_file: DocumentFileCreate):
        try:
            db_document_file = DocumentFile(
                document_id=document_file.document_id,
                provider=document_file.provider,
                bucket=document_file.bucket,
                storage_key=document_file.storage_key,
                original_filename=document_file.original_filename,
                mime_type=document_file.mime_type,
                size_bytes=document_file.size_bytes,
                checksum=document_file.checksum,
            )
            self.__db.add(db_document_file)
            await self.__db.flush()
            await self.__db.refresh(db_document_file)
        except Exception as e:
            logger.error("Failed to insert DocumentFile. Error: %s", str(e))
            raise
        return db_document_file
