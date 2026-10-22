# ADR 0002 — Backend stack

- Status: accepted
- Phase: 1

## Context

The backend must serve REST and WebSocket traffic, enforce validation, and stay
simple to deploy on Render while supporting async I/O for realtime features.

## Decision

- Python 3.12, FastAPI, Pydantic v2 for schemas and settings.
- SQLAlchemy 2.x async ORM with `asyncpg` and Alembic migrations.
- PostgreSQL 16 as the single relational store.
- One process serving both REST and WebSocket routes.
- `packages/contracts` is the source of truth for API shapes; backend routers
  and frontend clients are checked against it.

## Consequences

- Async end-to-end; blocking calls must be pushed to a thread pool.
- Migrations are mandatory for every schema change.
- Background work runs as in-process scheduled jobs until a dedicated worker is
  justified; the split is decided in Phase 16.