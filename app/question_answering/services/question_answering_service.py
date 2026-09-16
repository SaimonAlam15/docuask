from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.conversations.services.conversation_service import ConversationService
from app.documents.services.semantic_search_service import SemanticSearchService
from app.enums.conversation import ConversationMessageRole
from app.llm.base import LLMProvider
from app.llm.schemas.answer import LLMResponse


class QuestionAnsweringService:
    def __init__(
        self,
        session: AsyncSession,
        llm_provider: LLMProvider,
        search_service: SemanticSearchService,
        conversation_service: ConversationService,
    ):
        self.session = session
        self.llm_provider = llm_provider
        self.search_service = search_service
        self.conversation_service = conversation_service

    async def answer(self, question: str, conversation_id: UUID = None) -> LLMResponse:
        if not conversation_id:
            # Create conversation
            conversation_id = await self.conversation_service.create_conversation(
                user_id=UUID("77b03295-6eab-4d37-9429-2eeef614f278"),
            )
            await self.conversation_service.add_message(
                conversation_id=conversation_id,
                role=ConversationMessageRole.USER,
                content=question,
            )
        else:
            # Save question as conversation message
            await self.conversation_service.add_message(
                conversation_id=conversation_id, role=ConversationMessageRole.USER, content=question
            )
        search_results = await self.search_service.embed_and_search(question)

        if not search_results:
            return "No context found."

        context = [
            {
                "content": result.content,
                "document_content_id": result.document_content_id,
                "chunk_index": result.chunk_index,
            }
            for result, _ in search_results
        ]

        prompt = f"""
Answer the user's question using only the provided context which is in the form of a list of objects.
Once you have an answer, return it in the given json format.
Context: 
{context}

Question:
{question}
        """

        llm_response = await self.llm_provider.generate(prompt)

        # Save answer as conversation message
        await self.conversation_service.add_message(
            conversation_id=conversation_id,
            role=ConversationMessageRole.ASSISTANT,
            content=llm_response.answer,
        )

        await self.session.commit()

        return llm_response
