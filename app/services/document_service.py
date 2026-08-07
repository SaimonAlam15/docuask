import logging

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.document_file_repository import DocumentFileRepository
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentResponse
from app.schemas.document_file import DocumentFileCreate
from app.storage.base import StorageBackend

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(
        self,
        session: AsyncSession,
        doc_repo: DocumentRepository,
        doc_file_repo: DocumentFileRepository,
    ):
        self.session = session
        self.doc_repo = doc_repo
        self.doc_file_repo = doc_file_repo

    async def upload_file(
        self,
        file: UploadFile,
        document: DocumentCreate,
        storage: StorageBackend,
    ) -> DocumentResponse:
        storage_result = await storage.store(file)
        storage_key = storage_result.get("storage_key")
        checksum = storage_result.get("checksum")

        size = file.size
        mime_type = file.content_type
        filename = file.filename

        saved_document_file = None

        try:
            saved_document = await self.doc_repo.create_document(document)
            if saved_document:
                document_file = DocumentFileCreate(
                    document_id=saved_document.id,
                    provider="LOCAL",
                    storage_key=str(storage_key),
                    original_filename=filename,
                    mime_type=mime_type,
                    size_bytes=size,
                    checksum=checksum,
                )
                saved_document_file = await self.doc_file_repo.create_document_file(document_file)
                await self.session.commit()
        except Exception as e:
            logger.exception("Upload error: %s", str(e))
            raise

        return {
            "id": saved_document.id,
            "title": saved_document.title,
            "document_file": {
                "storage_key": saved_document_file.storage_key,
                "original_filename": saved_document_file.original_filename,
                "mime_type": saved_document_file.mime_type,
                "size_bytes": saved_document_file.size_bytes,
                "checksum": saved_document_file.checksum,
            },
        }
