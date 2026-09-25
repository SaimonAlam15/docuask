from unittest.mock import ANY, call

import pytest

import app.db.models
from app.conversations.models.conversation_message import ConversationMessage
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
            ),
            0.3,
        )
    ]
    fake_search_service.embed_and_search = mocker.AsyncMock(return_value=search_results)

    fake_llm_provider = mocker.MagicMock()
    fake_llm_response = LLMResponse(
        answer="Bangladesh became independent in 1971",
        sources=[Source(document_content_id="69c22e53-d610-492c-b8d5-8b858fb4c87e", chunk_index=1)],
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

    assert context == [
        {
            "content": res.content,
            "document_content_id": res.document_content_id,
            "chunk_index": res.chunk_index,
        }
        for res, _ in search_results
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

    fake_search_service = mocker.MagicMock()
    fake_search_service.embed_and_search = mocker.AsyncMock()

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
