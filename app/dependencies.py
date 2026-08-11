from collections.abc import AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.config import Settings
from app.repositories.document_file_repository import DocumentFileRepository
from app.repositories.document_repository import DocumentRepository
from app.storage.base import StorageBackend
from app.storage.local import LocalStorage


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


async def get_session(
    request: Request,
) -> AsyncGenerator[AsyncSession]:

    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory

    async with session_factory() as session:
        yield session


def get_storage_backend(settings: Settings = Depends(get_settings)) -> StorageBackend:
    # TODO: set backend according to env
    return LocalStorage(settings.storage.upload_directory.get_secret_value())


def get_document_repository(db: AsyncSession = Depends(get_session)) -> DocumentRepository:
    return DocumentRepository(db)


def get_document_file_repository(db: AsyncSession = Depends(get_session)) -> DocumentFileRepository:
    return DocumentFileRepository(db)
