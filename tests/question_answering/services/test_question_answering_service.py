import pytest

import app.db.models
from app.documents.models.document_chunk import DocumentChunk
from app.llm.schemas.answer import LLMResponse, Source
from app.question_answering.services.question_answering_service import QuestionAnsweringService


@pytest.mark.asyncio
async def test_search_results_empty(mocker):
    fake_llm_provider = mocker.MagicMock()
    fake_search_service = mocker.MagicMock()
    fake_search_service.embed_and_search = mocker.AsyncMock(return_value=[])

    qa_service = QuestionAnsweringService(
        llm_provider=fake_llm_provider, search_service=fake_search_service
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

    qa_service = QuestionAnsweringService(
        llm_provider=fake_llm_provider, search_service=fake_search_service
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

    fake_llm_provider.generate.assert_awaited_once_with(prompt)


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

    fake_llm_provider = mocker.MagicMock()
    fake_llm_provider.generate = mocker.AsyncMock(side_effect=RuntimeError("LLM Failed"))

    qa_service = QuestionAnsweringService(
        llm_provider=fake_llm_provider,
        search_service=fake_search_service,
    )

    with pytest.raises(RuntimeError, match="LLM Failed"):
        await qa_service.answer("When did Bangladesh become independent?")
