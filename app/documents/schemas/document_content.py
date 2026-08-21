from uuid import UUID

from pydantic import BaseModel


class DocumentContentCreate(BaseModel):
    document_id: UUID
    content: str
