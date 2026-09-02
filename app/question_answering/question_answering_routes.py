import logging

from fastapi import APIRouter, Body, Depends

from .dependencies import get_question_answering_service
from .services.question_answering_service import QuestionAnsweringService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/answer", response_model=None)
async def answer(
    question: str = Body(..., embed=True),
    question_answering_service: QuestionAnsweringService = Depends(get_question_answering_service),
):
    return await question_answering_service.answer(question)
