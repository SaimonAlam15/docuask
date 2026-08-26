import logging

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Settings
from app.documents.chunking.base import DocumentChunker
from app.documents.embeddings.base import EmbeddingProvider
from app.documents.extraction.base import DocumentExtractor
from app.documents.repositories.document_chunk_repository import DocumentChunkRepository
from app.documents.repositories.document_content_repository import DocumentContentRepository
from app.documents.repositories.document_file_repository import DocumentFileRepository
from app.documents.repositories.document_repository import DocumentRepository
from app.documents.schemas.document import DocumentCreate, DocumentResponse
from app.documents.schemas.document_chunk import DocumentChunkCreate
from app.documents.schemas.document_content import DocumentContentCreate
from app.documents.schemas.document_file import DocumentFileCreate
from app.storage.base import StorageBackend

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(
        self,
        session: AsyncSession,
        doc_repo: DocumentRepository,
        doc_file_repo: DocumentFileRepository,
        doc_content_repo: DocumentContentRepository,
        doc_chunk_repo: DocumentChunkRepository,
        extractor: DocumentExtractor,
        chunker: DocumentChunker,
        embedding_provider: EmbeddingProvider,
        settings: Settings,
    ):
        self.session = session
        self.doc_repo = doc_repo
        self.doc_file_repo = doc_file_repo
        self.doc_content_repo = doc_content_repo
        self.doc_chunk_repo = doc_chunk_repo
        self.extractor = extractor
        self.chunker = chunker
        self.embedding_provider = embedding_provider
        self.settings = settings

    async def upload_file(
        self,
        file: UploadFile,
        document: DocumentCreate,
        storage: StorageBackend,
    ) -> DocumentResponse:
        saved_document_file = None
        storage_key: str | None = None
        try:
            storage_result = await storage.store(file)
            storage_key = storage_result.storage_key
            checksum = storage_result.checksum

            size = file.size
            mime_type = file.content_type
            filename = file.filename
            saved_document = await self.doc_repo.create_document(document)
            if saved_document:
                document_file = DocumentFileCreate(
                    document_id=saved_document.id,
                    provider=self.settings.storage.provider,
                    storage_key=storage_key,
                    original_filename=filename,
                    mime_type=mime_type,
                    size_bytes=size,
                    checksum=checksum,
                )
                saved_document_file = await self.doc_file_repo.create_document_file(document_file)

                # Extract and save document content
                logger.info("Extracting document text...")
                extracted_content = self.extractor.extract_text(storage_key)
                document_content = DocumentContentCreate(
                    document_id=saved_document.id, content=extracted_content
                )
                saved_document_content = await self.doc_content_repo.create_document_content(
                    document_content
                )

                # Chunk the extracted content
                logger.info("Chunking document content...")
                chunks = self.chunker.chunk(extracted_content)
                document_chunks = []
                embeddings = await self.embedding_provider.embed(chunks)
                for idx, chunk in enumerate(chunks):
                    document_chunks.append(
                        DocumentChunkCreate(
                            document_content_id=saved_document_content.id,
                            content=chunk,
                            chunk_index=idx,
                            embedding=embeddings[idx],
                        )
                    )

                await self.doc_chunk_repo.create_document_chunks(document_chunks)

                await self.session.commit()
        except Exception as e:
            logger.exception("Upload error: %s", str(e))
            await self.session.rollback()
            if storage_key:
                try:
                    await storage.delete(storage_key)
                except Exception:
                    logger.error("Failed to clean up stored file: %s", storage_key)
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
