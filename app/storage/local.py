import hashlib
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from .base import StorageBackend
from .models import DocumentFileResult

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class LocalStorage(StorageBackend):
    async def store(self, file: UploadFile) -> DocumentFileResult:
        file_id = str(uuid4())
        filename = file.filename
        extension = filename.split(".")[-1]
        # size = file.size
        # mime_type = file.content_type
        path = UPLOAD_DIR / f"{file_id[:2]}/{file_id[2:4]}/{file_id}.{extension}"
        path.parent.mkdir(parents=True, exist_ok=True)
        sha256_hash = hashlib.sha256()

        try:
            with path.open("wb") as buffer:
                while chunk := await file.read(65536):
                    buffer.write(chunk)
                    sha256_hash.update(chunk)
        finally:
            await file.close()

        checksum = sha256_hash.hexdigest()

        return {"storage_key": path, "checksum": checksum}
