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
        user_id: UUID,
        session: AsyncSession,
        llm_provider: LLMProvider,
        search_service: SemanticSearchService,
        conversation_service: ConversationService,
    ):
        self.user_id = user_id
        self.session = session
        self.llm_provider = llm_provider
        self.search_service = search_service
        self.conversation_service = conversation_service

    async def answer(self, question: str, conversation_id: UUID | None = None) -> LLMResponse:
        conversation_messages = []

        if not conversation_id:
            # Create conversation
            conversation_id = await self.conversation_service.create_conversation(
                user_id=self.user_id,
            )
            await self.conversation_service.add_message(
                conversation_id=conversation_id,
                user_id=self.user_id,
                role=ConversationMessageRole.USER,
                content=question,
            )
        else:
            conversation_messages = await self.conversation_service.get_conversation_messages(
                conversation_id
            )
            conversation_history = "\n".join(
                [f"{cm.role}: {cm.content}" for cm in conversation_messages]
            )
            prompt = f"""
Rewrite the user's current question as a standalone question suitable for
semantic search.

Conversation history:
{conversation_history}

Current question:
{question}

Use the conversation history only when necessary to resolve references or
context that the current question depends on.

Rules:
- Preserve the meaning, intent, and scope of the current question.
- Resolve ambiguous references using the conversation history when possible.
- Replace pronouns and contextual references with the information they refer to
  when doing so makes the question self-contained.
- Do not introduce information that changes or unnecessarily narrows the
  question.
- Do not add details merely because they appear in the conversation history.
- Do not broaden the question beyond what the user asked.
- If the current question is already self-contained, keep it essentially
  unchanged.
- Return only the rewritten question. Do not answer it.

Rewritten question:
"""
            llm_response = await self.llm_provider.generate(prompt)
            question = llm_response.answer

            # Save question as conversation message
            await self.conversation_service.add_message(
                conversation_id=conversation_id,
                user_id=self.user_id,
                role=ConversationMessageRole.USER,
                content=question,
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
            user_id=self.user_id,
            role=ConversationMessageRole.ASSISTANT,
            content=llm_response.answer,
        )

        await self.session.commit()

        return llm_response
