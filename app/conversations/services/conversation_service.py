from uuid import UUID

from app.conversations.repositories.conversation_message_repository import (
    ConversationMessageRepository,
)
from app.conversations.repositories.conversation_repository import ConversationRepository
from app.conversations.schemas.conversation import ConversationCreate
from app.conversations.schemas.conversation_message import ConversationMessageCreate
from app.enums.conversation import ConversationMessageRole


class ConversationService:
    def __init__(self, repo: ConversationRepository, message_repo: ConversationMessageRepository):
        self.__conversation_repo = repo
        self.__message_repo = message_repo

    async def mnanage_conversation(
        self,
        user_id: UUID,
        role: ConversationMessageRole,
        content: str,
        conversation_id: UUID = None,
        title: str = None,
    ):
        if not conversation_id:
            db_conversation = await self.__conversation_repo.create_conversation(
                ConversationCreate(title=title, user_id=user_id)
            )
            conversation_id = db_conversation.id

        await self.__message_repo.create_conversation_message(
            ConversationMessageCreate(conversation_id=conversation_id, role=role, content=content)
        )

        return conversation_id
