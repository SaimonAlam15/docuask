from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.schemas.document import DocumentCreate


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_document(self, document: DocumentCreate):
        db_document = Document(title=document.title)
        try:
            self.db.add(db_document)
            await self.db.flush()
            await self.db.refresh(db_document)
        except Exception:
            await self.db.rollback()
            raise
        return db_document
