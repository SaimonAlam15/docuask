import os

from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter


class DoclingChunker:
    def __init__(self, max_tokens: int = 400) -> None:
        self.__chunker = HybridChunker(max_tokens=max_tokens, merge_peers=True)

    def chunk(self, filepath: str) -> list[(str, str)]:
        if not filepath:
            return []

        if not os.path.exists(filepath):
            return []

        converter = DocumentConverter()
        result = converter.convert(filepath)

        document = result.document

        chunks = []

        for chunk in self.__chunker.chunk(document):
            chunks.append(
                (
                    chunk.meta.headings or [],
                    chunk.text,
                )
            )

        return chunks
