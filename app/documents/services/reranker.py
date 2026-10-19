from sentence_transformers import CrossEncoder

from app.documents.models.document_chunk import DocumentChunk


class Reranker:
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(
        self, query: str, results: list[tuple[DocumentChunk, float]], top_k: int = 5
    ) -> list:
        if not results:
            return []

        print("Query", query)
        pairs = [(query, chunk.content) for chunk, _ in results]

        scores = self.model.predict(pairs)

        ranked_chunks = sorted(zip(results, scores), key=lambda item: float(item[1]), reverse=True)

        for c in ranked_chunks:
            print(f"id: {c[0][0].id}, score: {c[1]}")

        return [chunk for (chunk, _) in ranked_chunks[:top_k]]
