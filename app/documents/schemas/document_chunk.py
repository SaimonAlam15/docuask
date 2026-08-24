from uuid import UUID

from pydantic import BaseModel


class DocumentChunkCreate(BaseModel):
    document_content_id: UUID
    content: str
    chunk_index: int
    embedding: list[float]
