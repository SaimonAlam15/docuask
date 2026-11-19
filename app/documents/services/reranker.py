from sentence_transformers import CrossEncoder

from app.documents.models.document_chunk import DocumentChunk


class Reranker:
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self, query: str, results: list[tuple[DocumentChunk, float]], top_k: int = 5
    ) -> list:
        if not results:
            return []

        pairs = [
            (query, f"Section: {' > '.join(chunk.headings)}\n\n{chunk.content}")
            for chunk, _ in results
        ]

        scores = self.model.predict(pairs)

        ranked_chunks = sorted(zip(results, scores), key=lambda item: float(item[1]), reverse=True)

        return [
            (chunk[0], chunk[1], reranker_score)
            for (chunk, reranker_score) in ranked_chunks[:top_k]
        ]
