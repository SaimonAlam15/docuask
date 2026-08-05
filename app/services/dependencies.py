from fastapi import Depends

from app.dependencies import get_document_file_repository, get_document_repository
from app.repositories.document_file_repository import DocumentFileRepository
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService


def get_document_service(
    doc_repo: DocumentRepository = Depends(get_document_repository),
    doc_file_repo: DocumentFileRepository = Depends(get_document_file_repository),
) -> DocumentService:
    return DocumentService(doc_repo, doc_file_repo)
