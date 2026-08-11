from typing import Protocol

from fastapi import UploadFile

from .models import DocumentFileResult


class StorageBackend(Protocol):
    async def store(self, file: UploadFile, upload_directory: str) -> DocumentFileResult:
        pass

    async def exists(self, file_path: str) -> bool:
        pass

    async def delete(self, file_path: str) -> None:
        pass
