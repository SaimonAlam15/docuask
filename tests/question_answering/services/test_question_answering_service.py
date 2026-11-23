from unittest.mock import ANY, call

import pytest

import app.db.models
from app.conversations.models.conversation_message import ConversationMessage
from app.documents.models.document import Document
from app.documents.models.document_chunk import DocumentChunk
from app.llm.schemas.answer import LLMResponse, QueryRewriteResponse, Source
from app.question_answering.services.question_answering_service import QuestionAnsweringService


@pytest.mark.asyncio
async def test_search_results_empty(mocker):
    fake_llm_provider = mocker.MagicMock()
    fake_search_service = mocker.MagicMock()
    fake_search_service.embed_and_search = mocker.AsyncMock(return_value=[])

    fake_conversation_service = mocker.MagicMock
    fake_conversation_service.create_conversation = mocker.AsyncMock()
    fake_conversation_service.add_message = mocker.AsyncMock()
    fake_conversation_service.get_conversation_messages = mocker.AsyncMock()

    fake_session = mocker.MagicMock
    fake_session.commit = mocker.AsyncMock()

    qa_service = QuestionAnsweringService(
        user_id="f872e1ca-a14a-45c2-9913-e307cbc97636",
        session=fake_session,
        llm_provider=fake_llm_provider,
        search_service=fake_search_service,
        conversation_service=fake_conversation_service,
    )

    result = await qa_service.answer("")

    assert result == "No context found."
    fake_search_service.embed_and_search.assert_awaited_once_with("")


@pytest.mark.asyncio
async def test_llm_response(mocker):
    fake_search_service = mocker.MagicMock()
    search_results = [
        (
            DocumentChunk(
                content="Bangladesh became independent in 1971.",
                document_content_id="69c22e53-d610-492c-b8d5-8b858fb4c87e",
                chunk_index=1,
                headings=["Heading 1"],
            ),
            Document(title="Bangladesh Studies"),
            0.3,
        )
    ]
    fake_search_service.embed_and_search = mocker.AsyncMock(return_value=search_results)

    fake_llm_provider = mocker.MagicMock()
    fake_llm_response = LLMResponse(
        answer="Bangladesh became independent in 1971",
        sources=[Source(document_title="Bangladesh Studies", document_chunk_index=1)],
    )
    fake_llm_provider.generate = mocker.AsyncMock(return_value=fake_llm_response)

    fake_conversation_service = mocker.MagicMock
    fake_conversation_service.create_conversation = mocker.AsyncMock()
    fake_conversation_service.add_message = mocker.AsyncMock()
    fake_conversation_service.get_conversation_messages = mocker.AsyncMock()

    fake_session = mocker.MagicMock
    fake_session.commit = mocker.AsyncMock()

    qa_service = QuestionAnsweringService(
        user_id="f872e1ca-a14a-45c2-9913-e307cbc97636",
        session=fake_session,
        llm_provider=fake_llm_provider,
        search_service=fake_search_service,
        conversation_service=fake_conversation_service,
    )

    question = "When did Bangladesh become independent."

    result = await qa_service.answer(question)

    assert result == fake_llm_response

    fake_search_service.embed_and_search.assert_awaited_once_with(question)

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
{question}
        """

    assert context == [
        {
            "document_id": document.id,
            "document_title": document.title,
            "document_chunk_content": chunk.content,
            "document_chunk_headings": chunk.headings,
            "document_chunk_index": chunk.chunk_index,
        }
        for chunk, document, _ in search_results
    ]

    fake_llm_provider.generate.assert_awaited_once_with(prompt, LLMResponse)


@pytest.mark.asyncio
async def test_llm_failure(mocker):
    search_results = [
        (
            DocumentChunk(
                content="Bangladesh became independent in 1971.",
                document_content_id="69c22e53-d610-492c-b8d5-8b858fb4c87e",
                chunk_index=1,
            ),
            Document(title="Bangladesh Studies"),
            0.3,
        )
    ]
    fake_search_service = mocker.MagicMock()
    fake_search_service.embed_and_search = mocker.AsyncMock(return_value=search_results)

    fake_conversation_service = mocker.MagicMock
    fake_session = mocker.MagicMock

    fake_llm_provider = mocker.MagicMock()
    fake_llm_provider.generate = mocker.AsyncMock(side_effect=RuntimeError("LLM Failed"))

    qa_service = QuestionAnsweringService(
        user_id="f872e1ca-a14a-45c2-9913-e307cbc97636",
        session=fake_session,
        llm_provider=fake_llm_provider,
        search_service=fake_search_service,
        conversation_service=fake_conversation_service,
    )

    with pytest.raises(RuntimeError, match="LLM Failed"):
        await qa_service.answer("When did Bangladesh become independent?")


@pytest.mark.asyncio
async def test_follow_up_flow(mocker):
    fake_llm_provider = mocker.MagicMock()
    fake_query_rewrite_response = QueryRewriteResponse(
        query="What is Saimon Alam's designation?",
    )
    fake_llm_response = LLMResponse(
        answer="Saimon Alam is a Software Engineer",
        sources=[],
    )

    async def generate_side_effect(query, response_type):
        if response_type == QueryRewriteResponse:
            return fake_query_rewrite_response
        elif response_type == LLMResponse:
            return fake_llm_response

    fake_llm_provider.generate = mocker.AsyncMock(side_effect=generate_side_effect)

    search_results = [
        (
            DocumentChunk(
                content="Saimon Alam lives in Dhaka, Bangladesh. He was born there in 1990",
                document_content_id="69c22e53-d610-492c-b8d5-8b858fb4c87e",
                chunk_index=1,
            ),
            Document(title="Saimon Alam Resume"),
            0.3,
        )
    ]
    fake_search_service = mocker.MagicMock()
    fake_search_service.embed_and_search = mocker.AsyncMock(return_value=search_results)

    conversation_messages = [
        ConversationMessage(role="USER", content="Where does Saimon live?"),
        ConversationMessage(role="ASSISTANT", content="Saimon lives in Bangladesh."),
    ]
    fake_conversation_service = mocker.MagicMock
    fake_conversation_service.get_conversation_messages = mocker.AsyncMock(
        return_value=conversation_messages
    )

    fake_session = mocker.MagicMock

    qa_service = QuestionAnsweringService(
        user_id="f872e1ca-a14a-45c2-9913-e307cbc97636",
        session=fake_session,
        llm_provider=fake_llm_provider,
        search_service=fake_search_service,
        conversation_service=fake_conversation_service,
    )

    result = await qa_service.answer(
        "What is his designation?", "a872e1ca-a14a-45c2-9913-e307cbc97640"
    )
    assert result == fake_llm_response

    fake_search_service.embed_and_search.assert_awaited_once_with(
        "What is Saimon Alam's designation?"
    )

    assert fake_llm_provider.generate.await_count == 2

    fake_llm_provider.generate.assert_has_awaits(
        [call(ANY, QueryRewriteResponse), call(ANY, LLMResponse)], any_order=False
    )

    first_prompt, first_type = fake_llm_provider.generate.await_args_list[0].args
    second_prompt, second_type = fake_llm_provider.generate.await_args_list[1].args

    assert first_type is QueryRewriteResponse
    assert "What is his designation" in first_prompt
    assert "Where does Saimon live?" in first_prompt

    assert second_type is LLMResponse
    assert "What is Saimon Alam's designation?" in second_prompt
    assert "Saimon Alam lives in Dhaka, Bangladesh" in second_prompt
