import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health
from app.config import Settings
from app.db.session import create_engine, create_session_factory
from app.documents import document_routes, search_routes
from app.logging import configure_logging
from app.db import models
from app.question_answering import question_answering_routes

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
app.include_router(document_routes.router)
app.include_router(search_routes.router)
app.include_router(question_answering_routes.router)
