from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.documents.services.reranker import Reranker


def test_rerank_sorts_by_score_and_limits_results():
    chunks = [
        (SimpleNamespace(content="Chunk A"), 0.3),
        (SimpleNamespace(content="Chunk B"), 0.2),
        (SimpleNamespace(content="Chunk C"), 0.4),
    ]

    with patch("app.documents.services.reranker.CrossEncoder") as mock_encoder:
        model = MagicMock()
        model.predict.return_value = [0.2, 0.9, 0.5]
        mock_encoder.return_value = model

        reranker = Reranker()
        results = reranker.rerank("test question", chunks, top_k=2)

    assert [chunk.content for chunk, _ in results] == [
        "Chunk B",
        "Chunk C",
    ]
    assert len(results) == 2
