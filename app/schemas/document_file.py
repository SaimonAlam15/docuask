from uuid import UUID

from pydantic import BaseModel

from app.enums.storage_provider import StorageProvider


class FileUploadResult(BaseModel):
    storage_key: str
    original_filename: str
    mime_type: str
    size_bytes: int
    checksum: str


class DocumentFileCreate(BaseModel):
    document_id: UUID
    provider: StorageProvider
    bucket: str | None = None
    storage_key: str
    original_filename: str
    mime_type: str | None = None
    size_bytes: int
    checksum: str
