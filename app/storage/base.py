from typing import Protocol

from fastapi import UploadFile

from .models import DocumentFileResult


class StorageBackend(Protocol):
    async def store(self, file: UploadFile) -> DocumentFileResult:
        pass

    async def delete(self):
        pass

    async def exists(self):
        pass
