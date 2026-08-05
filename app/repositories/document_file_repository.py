from sqlalchemy.orm import Session

from app.models.document_file import DocumentFile
from app.schemas.document_file import DocumentFileCreate


class DocumentFileRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_document_file(self, document_file: DocumentFileCreate):
        print("In create document file")
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
            self.db.add(db_document_file)
            await self.db.commit()
            await self.db.refresh(db_document_file)
        except Exception:
            self.db.rollback()
            raise
        return db_document_file
