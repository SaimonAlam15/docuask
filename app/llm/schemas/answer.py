from pydantic import BaseModel, Field


class Source(BaseModel):
    document_title: str = Field(description="The title of the document the chunk belongs to.")
    document_chunk_index: int = Field(description="The numerical chunk index.")


class LLMResponse(BaseModel):
    answer: str = Field(
        description="The logical answer to the question based on the provided context."
    )
    sources: list[Source]


class QueryRewriteResponse(BaseModel):
    query: str
