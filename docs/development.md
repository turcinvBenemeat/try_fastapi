# Development notes

## Layering

- **`routers/`** — HTTP handlers; depend on `get_db` and return ORM objects or dicts; response models come from **`schemas/`**.  
- **`models/`** — SQLAlchemy table mappings; imported in `main.py` so `Base.metadata.create_all` sees every table.  
- **`database.py`** — Single `engine`, `SessionLocal`, and `get_db` dependency.  

To add a new resource: define ORM + Pydantic schemas, add a router, then `app.include_router(...)` in `src/main.py`.

## Database URL resolution

Order of precedence (see `src/database.py`):

1. `DATABASE_URL`  
2. Else `TEST_DATABASE_URL`  
3. Else `sqlite:///./sql_app.db`  

For **in-memory SQLite** (`sqlite:///:memory:`), the engine uses `StaticPool` so all connections share one database (required for tests and multi-request consistency).

## Logging

`src/logger.py` writes dated files under **`./logs`**. The directory is created if missing. Production Compose mounts a named volume at `/app/logs` so files persist across container restarts; development Compose bind-mounts `./logs`.

## Docker stages

| Stage | Contents |
|-------|----------|
| **production** | `requirements.txt`, app code, Uvicorn without `--reload`. No `curl`. |
| **development** | Everything above, plus `curl` (healthcheck in dev Compose) and `requirements-dev.txt`. |

Compose files are excluded from the image build context (`.dockerignore`), which is expected—they are only used on the host.

## Tests

- **`tests/conftest.py`** — Shared fixtures (e.g. HTTP client and DB session ordering).  
- The **`try-fastapi-tests`** service sets `DATABASE_URL=${TEST_DATABASE_URL}` so the app under test uses an isolated DB (e.g. in-memory) while `.env` may still point at a file DB for the running app.  

Run locally:

```bash
export PYTHONPATH=.
pytest tests -v
```

Run in Docker:

```bash
docker compose -f docker-compose.dev.yml run --rm try-fastapi-tests
```
