from fastapi import Depends

from app.config.settings import Settings
from app.dependencies import get_settings
from app.documents.dependencies import get_semantic_search_service
from app.documents.services.semantic_search_service import SemanticSearchService
from app.llm.base import LLMProvider
from app.llm.openai import OpenAILLMProvider
from app.question_answering.services.question_answering_service import QuestionAnsweringService


def get_openai_llm_provider(
    settings: Settings = Depends(get_settings),
) -> OpenAILLMProvider:
    return OpenAILLMProvider(settings.openai.api_key.get_secret_value(), settings.openai.llm_model)


def get_question_answering_service(
    llm_provider: LLMProvider = Depends(get_openai_llm_provider),
    search_service: SemanticSearchService = Depends(get_semantic_search_service),
) -> QuestionAnsweringService:
    return QuestionAnsweringService(llm_provider, search_service)
