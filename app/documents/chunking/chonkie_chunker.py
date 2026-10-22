from chonkie import RecursiveChunker


class ChonkieChunker:
    def __init__(self, chunk_size: int = 400, min_characters_per_chunk: int = 24) -> None:
        self.__chunker = RecursiveChunker(
            tokenizer="character",
            chunk_size=chunk_size,
            min_characters_per_chunk=min_characters_per_chunk,
        )

    def chunk(self, text: str) -> list[str]:
        if not text.strip():
            return []

        chunks = self.__chunker(text)

        return [chunk.text for chunk in chunks]
