FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN pip install --no-cache-dir uv

# Dependency layer
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# Application
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./

# Non-root user
RUN useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /app/uploads \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]