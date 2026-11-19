from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SearchResponse(BaseModel):
    id: UUID
    document_content_id: UUID
    content: str
    headings: list[str]
    chunk_index: int
    distance: float
    reranker_score: float
    created_at: datetime
