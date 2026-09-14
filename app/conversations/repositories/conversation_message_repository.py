from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.conversations.models.conversation_message import ConversationMessage
from app.conversations.schemas.conversation_message import ConversationMessageCreate


class ConversationMessageRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_conversation_message(self, conversation_message: ConversationMessageCreate):
        db_conversation_message = ConversationMessage(
            conversation_id=conversation_message.conversation_id,
            role=conversation_message.role,
            content=conversation_message.content,
        )
        self.__db.add(db_conversation_message)
        await self.__db.flush()
        await self.__db.refresh(db_conversation_message)
        return db_conversation_message

    async def get_conversation_by_id(self, conversation_message_id: UUID):
        query = select(ConversationMessage).where(ConversationMessage.id == conversation_message_id)
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def get_conversation_messages_by_conversation_id(self, conversation_id: UUID):
        query = select(ConversationMessage).where(
            ConversationMessage.conversation_id == conversation_id
        )
        result = await self.__db.execute(query)
        return result.all()
