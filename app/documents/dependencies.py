from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Settings
from app.dependencies import (
    get_session,
    get_settings,
)
from app.documents.repositories.document_file_repository import DocumentFileRepository
from app.documents.repositories.document_repository import DocumentRepository
from app.documents.services.document_service import DocumentService


def get_document_repository(db: AsyncSession = Depends(get_session)) -> DocumentRepository:
    return DocumentRepository(db)


def get_document_file_repository(db: AsyncSession = Depends(get_session)) -> DocumentFileRepository:
    return DocumentFileRepository(db)


def get_document_service(
    session: AsyncSession = Depends(get_session),
    doc_repo: DocumentRepository = Depends(get_document_repository),
    doc_file_repo: DocumentFileRepository = Depends(get_document_file_repository),
    settings: Settings = Depends(get_settings),
) -> DocumentService:
    return DocumentService(session, doc_repo, doc_file_repo, settings)
