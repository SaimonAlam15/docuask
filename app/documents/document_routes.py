import logging

from fastapi import APIRouter, Depends, File, UploadFile

from app.dependencies import get_storage_backend
from app.documents.dependencies import get_document_service
from app.documents.schemas.document import DocumentCreate
from app.documents.services.document_service import DocumentService
from app.storage.base import StorageBackend

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/documents", response_model=None)
async def create_document(
    file: UploadFile = File(...),
    document: DocumentCreate = Depends(DocumentCreate.as_form),
    document_service: DocumentService = Depends(get_document_service),
    storage_backend: StorageBackend = Depends(get_storage_backend),
):
    return await document_service.upload_file(file, document, storage_backend)
