import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import document, health
from app.config import Settings
from app.db.session import create_engine, create_session_factory
from app.logging import configure_logging

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

    logger.info("Application starting...")

    yield

    logger.info("Application shuttinf down...")


app = FastAPI(
    title="DocuAsk",
    lifespan=lifespan,
)


app.include_router(health.router)
app.include_router(document.router)
