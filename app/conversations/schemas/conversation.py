from uuid import UUID

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    title: str | None
    user_id: UUID
