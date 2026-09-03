from app.documents.services.semantic_search_service import SemanticSearchService
from app.llm.base import LLMProvider


class QuestionAnsweringService:
    def __init__(self, llm_provider: LLMProvider, search_service: SemanticSearchService):
        self.llm_provider = llm_provider
        self.search_service = search_service

    async def answer(self, question: str) -> str:
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

        return await self.llm_provider.generate(prompt)
