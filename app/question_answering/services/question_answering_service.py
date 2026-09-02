from app.documents.services.semantic_search_service import SemanticSearchService
from app.llm.base import LLMProvider


class QuestionAnsweringService:
    def __init__(self, llm_provider: LLMProvider, search_service: SemanticSearchService):
        self.llm_provider = llm_provider
        self.search_service = search_service

    async def answer(self, question: str) -> str:
        search_results = await self.search_service.embed_and_search(question)

        context = "\n\n".join(result.content for result, _ in search_results)

        prompt = f"""Answer the user's question using only the provided context.
        
        Context: 
        {context}

        Question:
        {question}
        """

        return await self.llm_provider.generate(prompt)
