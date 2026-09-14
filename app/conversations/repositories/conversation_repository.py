from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.conversations.models.conversation import Conversation
from app.conversations.schemas.conversation import ConversationCreate


class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_conversation(self, conversation: ConversationCreate):
        db_conversation = Conversation(title=conversation.title, user_id=conversation.user_id)
        self.__db.add(db_conversation)
        await self.__db.flush()
        await self.__db.refresh(db_conversation)
        return db_conversation

    async def get_conversation_by_id(self, conversation_id: UUID):
        query = select(Conversation).where(Conversation.id == conversation_id)
        result = await self.__db.execute(query)
        return result.scalar_one_or_none()

    async def get_conversations_by_user_id(self, user_id: UUID):
        query = select(Conversation).where(Conversation.user_id == user_id)
        result = await self.__db.execute(query)
        return result.all()
