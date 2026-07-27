from fastapi import APIRouter, Depends

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import Settings
from app.dependencies import get_settings, get_session

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


@router.get('/health/database')
async def database_health(
    session: AsyncSession = Depends(get_session)
):
    await session.execute(text("SELECT 1"))

    return {
        "status": "healthy",
    }