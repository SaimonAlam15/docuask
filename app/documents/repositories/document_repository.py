import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.models.document import Document
from app.documents.schemas.document import DocumentCreate

logger = logging.getLogger(__name__)


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_document(self, document: DocumentCreate):
        db_document = Document(title=document.title)
        try:
            self.__db.add(db_document)
            await self.__db.flush()
            await self.__db.refresh(db_document)
        except Exception as e:
            logger.error("Failed to insert Document. Error: %s", str(e))
            raise
        return db_document
