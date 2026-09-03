from pydantic import BaseModel, Field


class Source(BaseModel):
    document_content_id: str = Field(description="The id of the content the chunk belongs to.")
    chunk_index: int = Field(description="The numerical chunk index.")


class LLMResponse(BaseModel):
    answer: str = Field(
        description="The logical answer to the question based on the provided context."
    )
    sources: list[Source]
