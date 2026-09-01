import logging

from fastapi import APIRouter, Body, Depends

from app.documents.dependencies import get_semantic_search_service
from app.documents.schemas.search import SearchResponse
from app.documents.services.semantic_search_service import SemanticSearchService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/search", response_model=list[SearchResponse])
async def search(
    query: str = Body(..., embed=True),
    search_service: SemanticSearchService = Depends(get_semantic_search_service),
):
    result = await search_service.embed_and_search(query)
    res: list[SearchResponse] = []
    for obj in result:
        res.append(
            SearchResponse(
                document_content_id=obj[0].document_content_id,
                content=obj[0].content,
                chunk_index=obj[0].chunk_index,
                created_at=obj[0].created_at,
                distance=obj[1],
            )
        )
    return res
