from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from app.config import Settings
from app.api.routes import health
from app.logging import configure_logging
from app.database import create_engine, create_session_factory


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    
    settings = Settings()

    engine = create_engine(settings)
    session_factory = create_session_factory(engine)
    
    app.state.settings = settings
    app.state.engine = engine
    app.state.session_factory = session_factory

    logger.info('Application starting...')

    yield

    logger.info("Application shuttinf down...")


app = FastAPI(
    title="DocuAsk",
    lifespan=lifespan,
)


app.include_router(health.router)