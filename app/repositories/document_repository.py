from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.document import DocumentCreate


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_document(self, document: DocumentCreate):
        db_document = Document(title=document.title)
        try:
            self.db.add(db_document)
            await self.db.commit()
            await self.db.refresh(db_document)
        except Exception:
            self.db.rollback()
            raise
        return db_document
