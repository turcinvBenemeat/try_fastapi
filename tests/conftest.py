from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.database import engine, SessionLocal
from src.models.tasks import Base

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy ``Session`` for one test function.

    Before each test, **drops and recreates** all tables bound to ``Base`` so
    the database starts from a clean schema (useful for predictable primary keys
    and no cross-test data leakage).

    Yields:
        Session: Open session; the test may commit or rollback as needed.

    Note:
        Closing the session does not drop tables; the next test run repeats
        ``drop_all`` / ``create_all``.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """
    Provide a Starlette/FastAPI ``TestClient`` for issuing HTTP calls to ``app``.

    Uses the context-manager form so startup/shutdown events and the ASGI lifespan
    (if any) are respected around the test.

    Yields:
        TestClient: Client with ``.get``, ``.post``, etc., against the same
        ``app`` instance imported from ``src.main``.
    """
    with TestClient(app) as test_client:
        yield test_client

