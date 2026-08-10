import asyncio
import hashlib
import logging
import os
from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from .base import StorageBackend
from .models import DocumentFileResult

logger = logging.getLogger(__name__)


class LocalStorage(StorageBackend):
    async def store(self, file: UploadFile, upload_directory: str) -> DocumentFileResult:
        UPLOAD_DIR = Path(upload_directory)
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        file_id = str(uuid4())
        filename = file.filename
        extension = filename.split(".")[-1]
        # size = file.size
        # mime_type = file.content_type
        path = UPLOAD_DIR / f"{file_id[:2]}/{file_id[2:4]}/{file_id}.{extension}"
        path.parent.mkdir(parents=True, exist_ok=True)
        sha256_hash = hashlib.sha256()

        try:
            async with aiofiles.open(path, "wb") as buffer:
                while chunk := await file.read(65536):
                    await buffer.write(chunk)
                    sha256_hash.update(chunk)
        finally:
            await file.close()

        checksum = sha256_hash.hexdigest()

        return DocumentFileResult(storage_key=str(path), checksum=checksum)

    async def exists(self, file_path: str) -> bool:
        if await aiofiles.os.path.exists(file_path):
            logger.info("The file or directory exists.")
            return True
        else:
            logger.info("File not found.")
        return False

    async def delete(self, file_path: str) -> bool:
        if self.exists(file_path):
            try:
                await asyncio.to_thread(os.remove, file_path)
                logger.info("Successfully deleted %s", file_path)
                return True
            except PermissionError:
                logger.error("Error: Insufficient permissions to delete %s", file_path)
        return False
