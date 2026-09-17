from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.conversations.repositories.conversation_message_repository import (
    ConversationMessageRepository,
)
from app.conversations.repositories.conversation_repository import ConversationRepository
from app.conversations.services.conversation_service import ConversationService
from app.dependencies import get_session


def get_conversation_repository(db: AsyncSession = Depends(get_session)) -> ConversationRepository:
    return ConversationRepository(db)


def get_conversation_message_repository(
    db: AsyncSession = Depends(get_session),
) -> ConversationMessageRepository:
    return ConversationMessageRepository(db)


def get_conversation_service(
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
    conversation_message_repository: ConversationMessageRepository = Depends(
        get_conversation_message_repository
    ),
) -> ConversationService:
    return ConversationService(conversation_repository, conversation_message_repository)
