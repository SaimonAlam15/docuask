from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.conversations.services.conversation_service import ConversationService
from app.documents.services.semantic_search_service import SemanticSearchService
from app.enums.conversation import ConversationMessageRole
from app.llm.base import LLMProvider
from app.llm.schemas.answer import LLMResponse, QueryRewriteResponse


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
        final_question = question

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
            llm_response = await self.llm_provider.generate(prompt, QueryRewriteResponse)
            final_question = llm_response.query

            # Save question as conversation message
            await self.conversation_service.add_message(
                conversation_id=conversation_id,
                user_id=self.user_id,
                role=ConversationMessageRole.USER,
                content=question,
                rewritten_query=final_question,
            )

        search_results = await self.search_service.embed_and_search(final_question)

        if not search_results:
            return "No context found."

        context = [
            {
                "document_id": document.id,
                "document_title": document.title,
                "document_chunk_content": chunk.content,
                "document_chunk_headings": chunk.headings,
                "document_chunk_index": chunk.chunk_index,
            }
            for chunk, document, _ in search_results
        ]

        prompt = f"""
Answer the user's question using only the provided context which is in the form of a list of objects.
Once you have an answer, return it in the given json format.
Context: 
{context}

Source Attribution and Context:
- Treat each document as a distinct source of information. Use its title to identify the source, but do not assume that the filename accurately describes its contents or identifies the person or entity discussed.
- Documents belonging to the same user may concern different people, organizations, or subjects. Never assume they all describe the user or the same entity.
- You may combine information from multiple documents and chunks when answering questions, provided the information is relevant and the sources support the conclusions.
- Preserve the distinction between information found in different documents. Do not attribute information from one document to a person or entity mentioned in another without supporting evidence.
- When the subject of a document or a piece of information cannot be established from the available context, do not guess. Explain the ambiguity when it affects the answer.
- If sources contradict one another, acknowledge the discrepancy rather than arbitrarily choosing one version.
- Base answers on the provided context. Do not invent missing information or make unsupported assumptions.


Contextual Interpretation:
Interpret retrieved information in the context of its document structure, headings, and surrounding content.

You may make reasonable inferences from conventional document layouts and clearly established relationships. For example, an institution listed under an individual's education or degree section in their résumé can be treated as the institution associated with that qualification.

Do not require information to be explicitly stated in a complete sentence when its meaning is clear from the document structure.

However, distinguish reasonable contextual inferences from unsupported assumptions. If the document structure does not establish the relationship with sufficient confidence, acknowledge the uncertainty.


Answering Rules:
- Answer questions using the information available in the retrieved context.
- Prioritize directly relevant evidence over information that is merely topically related.
- When multiple chunks or documents contain relevant information, combine them when appropriate to provide a complete answer.
- Do not omit important details necessary to answer the question accurately.
- Do not introduce facts, assumptions, or external knowledge that are not supported by the retrieved context.
- If the context provides enough information to answer the question, answer directly and confidently. Do not unnecessarily express uncertainty or demand explicit wording when the meaning is clear.
- If the context provides only partial information, answer what can be established and clearly identify what remains unknown.
- If the context does not contain sufficient information to answer the question, explicitly state that the information is unavailable. Do not guess or fabricate an answer.
- If retrieved sources contradict one another, acknowledge the conflicting information and identify the relevant sources.
- Keep answers focused on the question. Avoid unnecessary explanations or unrelated information.
- Ensure that every factual claim in the answer is supported by the retrieved context.
- Include source references for the information used in the answer, following the application's expected source-reference format.

Question:
{final_question}
        """

        llm_response = await self.llm_provider.generate(prompt, LLMResponse)

        # Save answer as conversation message
        await self.conversation_service.add_message(
            conversation_id=conversation_id,
            user_id=self.user_id,
            role=ConversationMessageRole.ASSISTANT,
            content=llm_response.answer,
        )

        await self.session.commit()

        return llm_response
