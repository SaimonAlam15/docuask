from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from app.config import Settings
from app.api.routes import health
from app.logging import configure_logging


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    
    settings = Settings()
    
    app.state.settings = settings

    logger.info('Application starting...')

    yield

    logger.info("Application shuttinf down...")


app = FastAPI(
    title="DocuAsk",
    lifespan=lifespan,
)


app.include_router(health.router)