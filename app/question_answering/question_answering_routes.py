from fastapi import APIRouter, Body, Depends

from .dependencies import get_question_answering_service
from .services.question_answering_service import QuestionAnsweringService

router = APIRouter()


@router.post("/answer")
async def answer(
    question: str = Body(..., embed=True),
    question_answering_service: QuestionAnsweringService = Depends(get_question_answering_service),
):
    return await question_answering_service.answer(question)
