from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM as PGENUM
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.storage_provider import StorageProvider

if TYPE_CHECKING:
    from .document import Document


class DocumentFile(Base):
    __tablename__ = "document_files"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    document_id: Mapped[UUID] = mapped_column(ForeignKey("documents.id"), nullable=False)

    document: Mapped[Document] = relationship(back_populates="files")

    provider: Mapped[StorageProvider] = mapped_column(
        PGENUM(StorageProvider, name="storage_provider"),
        default=StorageProvider.LOCAL,
        nullable=False,
    )

    bucket: Mapped[str | None] = mapped_column(String(255), nullable=True)

    storage_key: Mapped[str] = mapped_column(Text, nullable=False)

    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)

    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)

    checksum: Mapped[str] = mapped_column(String(64), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_document_file_checksum", "checksum"),
        UniqueConstraint("provider", "bucket", "storage_key"),
    )
