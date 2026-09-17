from uuid import UUID

from pydantic import BaseModel

from app.enums.conversation import ConversationMessageRole


class ConversationMessageCreate(BaseModel):
    conversation_id: UUID
    role: ConversationMessageRole
    content: str
