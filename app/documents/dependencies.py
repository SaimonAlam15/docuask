from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Settings
from app.dependencies import (
    get_session,
    get_settings,
)
from app.documents.extraction.base import DocumentExtractor
from app.documents.extraction.pdf import PDFExtractor
from app.documents.repositories.document_content_repository import DocumentContentRepository
from app.documents.repositories.document_file_repository import DocumentFileRepository
from app.documents.repositories.document_repository import DocumentRepository
from app.documents.services.document_service import DocumentService


def get_document_repository(db: AsyncSession = Depends(get_session)) -> DocumentRepository:
    return DocumentRepository(db)


def get_document_file_repository(db: AsyncSession = Depends(get_session)) -> DocumentFileRepository:
    return DocumentFileRepository(db)


def get_document_content_repository(
    db: AsyncSession = Depends(get_session),
) -> DocumentContentRepository:
    return DocumentContentRepository(db)


def get_pdf_extractor() -> PDFExtractor:
    return PDFExtractor()


def get_document_service(
    session: AsyncSession = Depends(get_session),
    doc_repo: DocumentRepository = Depends(get_document_repository),
    doc_file_repo: DocumentFileRepository = Depends(get_document_file_repository),
    doc_content_repo: DocumentContentRepository = Depends(get_document_content_repository),
    extractor: DocumentExtractor = Depends(get_pdf_extractor),
    settings: Settings = Depends(get_settings),
) -> DocumentService:
    return DocumentService(session, doc_repo, doc_file_repo, doc_content_repo, extractor, settings)
