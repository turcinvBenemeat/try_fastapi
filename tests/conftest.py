from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.main import app
from src.database import Base, engine, SessionLocal


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
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    HTTP client against ``app``. Depends on ``db_session`` so the schema is reset
    before the client is used (stable order across pytest versions).
    """
    with TestClient(app) as test_client:
        yield test_client
