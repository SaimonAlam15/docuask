from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SearchResponse(BaseModel):
    id: UUID
    document_content_id: UUID
    content: str
    chunk_index: int
    distance: float
    created_at: datetime
