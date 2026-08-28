import logging

from fastapi import APIRouter, Body, Depends, File, UploadFile

from app.dependencies import get_storage_backend
from app.documents.dependencies import get_document_service, get_semantic_search_service
from app.documents.schemas.document import DocumentCreate
from app.documents.services.document_service import DocumentService
from app.documents.services.semantic_search_service import SemanticSearchService
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


@router.post("/search", response_model=None)
async def search(
    query: str = Body(..., embed=True),
    search_service: SemanticSearchService = Depends(get_semantic_search_service),
):
    return await search_service.embed_and_search(query)
