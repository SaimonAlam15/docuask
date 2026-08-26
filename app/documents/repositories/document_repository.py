from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.models.document import Document
from app.documents.schemas.document import DocumentCreate


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_document(self, document: DocumentCreate):
        db_document = Document(title=document.title)
        self.__db.add(db_document)
        await self.__db.flush()
        await self.__db.refresh(db_document)
        return db_document
