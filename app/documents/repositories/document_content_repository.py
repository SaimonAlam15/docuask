from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.models.document_content import DocumentContent
from app.documents.schemas.document_content import DocumentContentCreate


class DocumentContentRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_document_content(self, document_content: DocumentContentCreate):
        db_document_content = DocumentContent(
            document_id=document_content.document_id, content=document_content.content
        )
        self.__db.add(db_document_content)
        await self.__db.flush()
        await self.__db.refresh(db_document_content)
        return db_document_content
