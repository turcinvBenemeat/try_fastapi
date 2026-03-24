# try_fastapi

Small **FastAPI** app with **SQLAlchemy 2**, **SQLite** by default, and **APIRouter** modules for **tasks** and **projects**. Includes **pytest** + **TestClient** tests.

## Requirements

- Docker & Docker Compose, *or*
- Python 3.12+ and a virtual environment

## Configuration

Copy `.env.example` to `.env` and adjust if needed:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | App database (default: file SQLite) |
| `TEST_DATABASE_URL` | Test DB (e.g. `sqlite:///:memory:`); test service sets `DATABASE_URL` from this |
| `PYTHONPATH` | Set to `.` so `src.main` and package imports resolve |

## API overview

| Prefix | Notes |
|--------|--------|
| `GET /` | Liveness JSON (`message`) |
| `/tasks` | List, create (`GET`/`POST` on `/tasks`), get/update/delete by id |
| `/projects` | Same CRUD pattern as tasks |

OpenAPI UI: [http://localhost:8000/docs](http://localhost:8000/docs) when the app is running.

**HTTP behavior (both resources):** success responses use **200** with JSON bodies; missing rows return **404** with `{"detail": "…"}`; invalid bodies return **422**. Deletes return `{"message": "…"}`.

**Data model:** `Task` may reference `Project` via optional `project_id` (see `src/models`).

## Run with Docker

```bash
docker compose up try-fastapi
```

- API: [http://localhost:8000](http://localhost:8000)

```bash
docker compose run --rm try-fastapi-tests
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then edit as above
```

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
pytest tests
```

## Layout

| Path | Role |
|------|------|
| `src/main.py` | App, `include_router`, `Base.metadata.create_all`, root `GET /` |
| `src/routers/__init__.py` | Re-exports `tasks_router`, `projects_router` |
| `src/routers/tasks.py` | Task CRUD under `/tasks` |
| `src/routers/projects.py` | Project CRUD under `/projects` |
| `src/database.py` | Engine (incl. in-memory `StaticPool` when needed), `SessionLocal`, `get_db`, `Base` |
| `src/models/tasks.py`, `src/models/projects.py` | SQLAlchemy models (`Task` ↔ `Project`) |
| `src/schemas/tasks.py`, `src/schemas/projects.py` | Pydantic API schemas (`*Create`, read models) |
| `src/logger.py` | Logging helper |
| `tests/conftest.py` | `client`, `db_session` fixtures |
| `tests/test_main.py` | Root route |
| `tests/test_tasks.py` | `/tasks` integration tests |
| `tests/test_projects.py` | `/projects` integration tests |
