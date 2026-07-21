from fastapi import APIRouter, Depends

from app.config import Settings
from app.dependencies import get_settings

import logging


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/health')
async def health(
    settings: Settings = Depends(get_settings),
):
    logger.info('Health check requested')

    return {
        "status": "healthy",
        "application": settings.app.name
    }