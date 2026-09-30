# DocuAsk

DocuAsk is an async FastAPI service for document ingestion, semantic retrieval, and question answering with conversation-aware follow-ups.

Documents are extracted, chunked, embedded, and stored in PostgreSQL with `pgvector`. Questions are answered through semantic retrieval, while conversation history and query rewriting allow follow-up questions to be resolved in context. The final response includes source references for the retrieved information.

## Highlights

- Upload and persist documents
- Extract, chunk, and embed document content
- Semantic search using PostgreSQL + `pgvector`
- LLM-based answers with source references
- Conversation-aware follow-up questions
- Query rewriting for context-dependent questions
- Fully Dockerized development and production-style environments
- Dedicated Compose migration service
- Makefile-based developer workflow
- GitHub Actions CI

## Architecture

```text
Document
   │
   ▼
Extract
   │
   ▼
Chunk
   │
   ▼
Embed
   │
   ▼
PostgreSQL + pgvector
   │
   │
Question ──► Conversation History
   │
   ▼
Query Rewriting
   │
   ▼
Semantic Retrieval
   │
   ▼
LLM
   │
   ▼
Answer + Sources
```

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy with `AsyncSession`
- PostgreSQL + `pgvector`
- Redis
- Docker + Docker Compose
- Alembic
- `uv`
- GitHub Actions

## Project Structure

```text
app/
tests/
migrations/
.github/
└── workflows/
    └── ci.yaml

Dockerfile
compose.yaml
compose.dev.yaml
Makefile
alembic.ini
pyproject.toml
```

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- `make`

## Configuration

Create a `.env` file containing the required application configuration.

For local development, keep your `.env` file out of version control and use your own credentials/configuration.

## Makefile Commands

```bash
make dev
make prod
make dev-down
make prod-down
make logs
```

Use `make dev` for the development environment and `make prod` for the production-style Compose configuration.

## Quick Start

### Development

1. Create your `.env` file.
2. Start the development stack:

```bash
make dev
```

3. Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

4. Stop the development stack:

```bash
make dev-down
```

### Production-style Run

Build and start the production-style stack:

```bash
make prod
```

Stop it with:

```bash
make prod-down
```

## Database Migrations

Database migrations are handled by a dedicated Docker Compose `migration` service.

When the containerized stack starts, the migration service runs the Alembic migrations before the application becomes available.

No separate migration command is required for the standard Docker workflow.

Migration files are version-controlled and validated in CI.

## Testing

With the development stack running:

```bash
docker compose -f compose.yaml -f compose.dev.yaml exec app uv run pytest -q
```

## CI

GitHub Actions runs the CI workflow defined in:

```text
.github/workflows/ci.yaml
```

The CI pipeline:

- Installs dependencies using `uv`
- Starts PostgreSQL with `pgvector`
- Starts Redis
- Validates the Alembic migration history
- Checks that there is a single migration head
- Runs migrations against a fresh database
- Runs the test suite
- Builds the Docker image after tests pass

This ensures that the database can be constructed from the version-controlled migration history and that the application passes its test suite in a clean environment.
