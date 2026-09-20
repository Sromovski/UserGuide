# [SERVICE NAME] — Python API

[One sentence describing what this service does and who calls it.]

## Tech stack

- Python [3.12], FastAPI [0.115], Pydantic v2
- DB: [PostgreSQL] via [SQLAlchemy 2.0 async] + [Alembic] migrations
- Tests: pytest + httpx AsyncClient
- Env/deps: [uv] ([poetry] / [pip-tools])
- Lint/format: [ruff]

## Commands

```bash
uv sync                          # install
uv run uvicorn app.main:app --reload
uv run pytest -q                 # tests
uv run pytest --cov=app          # with coverage
uv run ruff check . && uv run ruff format --check .
uv run alembic upgrade head      # apply migrations
```

Done means: `uv run pytest -q` and `uv run ruff check .` both pass.

## Architecture

- `app/main.py`      — app factory and router registration
- `app/api/`         — routers, one module per resource. Thin: validate, delegate, return.
- `app/services/`    — business logic. No FastAPI imports in here.
- `app/models/`      — SQLAlchemy models
- `app/schemas/`     — Pydantic request/response models
- `app/db.py`        — session management
- `tests/`           — mirrors the `app/` layout

Request flow: router -> schema validation -> service -> repository -> DB.

## Conventions

- Type-annotate every function signature.
- Routers never touch the DB session directly — go through a service.
- Raise `HTTPException` only in the router layer; services raise domain errors.
- All I/O is `async`. Never call a blocking library inside an async handler.
- Pydantic schemas are the API contract — changing one is a breaking change.
- Log with structured fields, never f-strings containing user data.

## Boundaries

- Never edit files in `alembic/versions/` — generate a new migration instead.
- Never read or print `.env`, and never log secrets or full request bodies.
- Do not add a dependency without asking.
- `app/auth/` requires review — flag changes, do not silently refactor.

## Build rules

1. Write a failing test that reproduces the bug before fixing it.
2. Schema change => migration in the same commit.
3. Run the full test suite before saying done, and paste the output.
4. Keep functions under ~40 lines; extract rather than nest.
