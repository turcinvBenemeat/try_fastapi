# try_fastapi

Small **FastAPI** service with **SQLAlchemy 2**, **SQLite** by default, and **pytest** + **TestClient** tests.

## Requirements

- Docker & Docker Compose, *or*
- Python 3.12+ and a virtual environment

## Configuration

Copy `.env.example` to `.env` and adjust if needed:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | App database (default: file SQLite) |
| `TEST_DATABASE_URL` | Tests (e.g. `sqlite:///:memory:`) |
| `PYTHONPATH` | Use `.` so imports like `src.main` resolve |

## Run with Docker

```bash
docker compose up try-fastapi
```

- API: [http://localhost:8000](http://localhost:8000)  
- OpenAPI UI: [http://localhost:8000/docs](http://localhost:8000/docs)

Run the test container:

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

- `src/main.py` — app, routes, DB dependency  
- `src/database.py` — engine, session, `Base`  
- `src/models.py` — SQLAlchemy models  
- `src/schemas.py` — Pydantic request/response schemas  
- `tests/` — pytest + `conftest.py` fixtures  
