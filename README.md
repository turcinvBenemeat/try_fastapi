# try_fastapi

Small **FastAPI** app with **SQLAlchemy 2**, **SQLite** by default, **APIRouter**-based routes, and **pytest** + **TestClient**.

## Requirements

- Docker & Docker Compose, *or*
- Python 3.12+ and a virtual environment

## Configuration

Copy `.env.example` to `.env` and adjust if needed:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | App database (default: file SQLite) |
| `TEST_DATABASE_URL` | Test DB (e.g. `sqlite:///:memory:`; compose passes this as `DATABASE_URL` in the test service) |
| `PYTHONPATH` | Set to `.` so `src.main` and friends resolve |

## Run with Docker

```bash
docker compose up try-fastapi
```

- API: [http://localhost:8000](http://localhost:8000)  
- OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)

Tests:

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
| `src/main.py` | `FastAPI` app, `include_router`, root `GET /` |
| `src/routers/tasks.py` | Task CRUD under `/tasks` |
| `src/routers/projects.py` | Placeholder for more routers |
| `src/database.py` | Engine, `SessionLocal`, `get_db`, `Base` |
| `src/models/tasks.py` | SQLAlchemy `Task` model |
| `src/schemas/tasks.py` | Pydantic `Task` / `TaskCreate` schemas |
| `src/logger.py` | Logging helper |
| `tests/conftest.py` | `client`, `db_session` fixtures |
| `tests/test_main.py` | App / root route |
| `tests/test_tasks.py` | `/tasks` API |
