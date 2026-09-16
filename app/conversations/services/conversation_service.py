from uuid import UUID

from app.conversations.models.conversation_message import ConversationMessage
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

    async def create_conversation(
        self,
        user_id: UUID,
        title: str | None = None,
    ):
        db_conversation = await self.__conversation_repo.create_conversation(
            ConversationCreate(title=title, user_id=user_id)
        )
        conversation_id = db_conversation.id

        return conversation_id

    async def add_message(
        self,
        conversation_id: UUID,
        role: ConversationMessageRole,
        content: str,
    ):
        await self.__message_repo.create_conversation_message(
            ConversationMessageCreate(conversation_id=conversation_id, role=role, content=content)
        )

    async def get_conversation_messages(
        self, conversation_id: UUID
    ) -> list[ConversationMessage] | None:
        return await self.__message_repo.get_messages_by_conversation_id(conversation_id)
