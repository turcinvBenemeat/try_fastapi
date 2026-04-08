# Task Manager API

A small [FastAPI](https://fastapi.tiangolo.com/) service for **projects** and **tasks**, backed by [SQLAlchemy](https://www.sqlalchemy.org/) 2.x. Tables are created on startup (`create_all`). Interactive API docs are served at **`/docs`** (Swagger UI) and **`/redoc`**.

## Stack

- Python 3.12, FastAPI, Uvicorn  
- SQLAlchemy 2.0 (default: SQLite file `sql_app.db` in the working directory)  
- Optional Docker multi-stage build: **production** vs **development** images  

## Quick start (local)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # optional; defaults match example
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for a simple JSON health-style message, or [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the full API.

## Configuration

Copy [`.env.example`](./.env.example) to `.env` and adjust as needed.

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | SQLAlchemy URL for the app (e.g. `sqlite:///./sql_app.db` or Postgres). |
| `TEST_DATABASE_URL` | Used in tests when `DATABASE_URL` is unset (e.g. `sqlite:///:memory:` in Docker Compose). |
| `PYTHONPATH` | Set to `.` for local runs so `src` imports resolve (Docker sets `/app`). |

If neither `DATABASE_URL` nor `TEST_DATABASE_URL` is set, the app falls back to `sqlite:///./sql_app.db`.

## API overview

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Liveness response (does not check the database). |
| `GET` | `/tasks` | List tasks. |
| `GET` | `/tasks/{task_id}` | Get a task. |
| `POST` | `/tasks` | Create a task (JSON: `title`, optional `description`, `completed`, optional `project_id`). |
| `PUT` | `/tasks/{task_id}` | Update a task (same body shape as create). |
| `DELETE` | `/tasks/{task_id}` | Delete a task. |
| `GET` | `/projects` | List projects. |
| `GET` | `/projects/{project_id}` | Get a project. |
| `POST` | `/projects` | Create a project (`name`, optional `description`, optional `is_active`). |
| `PUT` | `/projects/{project_id}` | Update a project. |
| `DELETE` | `/projects/{project_id}` | Delete a project. |

Prefer **`/docs`** for request/response schemas and try-it-out calls.

## Docker

| Compose file | Use case |
|--------------|----------|
| [`docker-compose.yml`](./docker-compose.yml) | **Production**: `target: production`, code baked in, named volume for `./logs`, healthcheck via Python. |
| [`docker-compose.dev.yml`](./docker-compose.dev.yml) | **Development**: bind mounts for `src`, Uvicorn `--reload`, optional **`try-fastapi-tests`** service. |

```bash
# Production (default)
docker compose up -d

# Local development (+ hot reload)
docker compose -f docker-compose.dev.yml up
```

Image build targets are defined in the [`Dockerfile`](./Dockerfile): **production** (runtime deps only) and **development** (adds `curl`, dev/requirements).

## Tests

Install dev dependencies, then run pytest from the repo root (`PYTHONPATH` should include the project root; `.env.example` sets `PYTHONPATH=.`).

```bash
pip install -r requirements-dev.txt
pytest tests
```

With Docker Compose (dev file), the test service overrides `DATABASE_URL` from `TEST_DATABASE_URL`:

```bash
docker compose -f docker-compose.dev.yml run --rm try-fastapi-tests
```

## Project layout

```text
src/
  main.py              # FastAPI app, routers, create_all
  database.py          # engine, sessions, get_db
  logger.py            # file logging under ./logs
  models/              # SQLAlchemy ORM models
  schemas/             # Pydantic request/response models
  routers/             # API routes
tests/                 # pytest + httpx
```

More detail for contributors (database behavior, Docker stages, extending the API): [`docs/development.md`](./docs/development.md).
