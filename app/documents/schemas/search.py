from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SearchResponse(BaseModel):
    document_content_id: UUID
    content: str
    chunk_index: int
    distance: float
    created_at: datetime
