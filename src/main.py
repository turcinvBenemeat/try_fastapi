from typing import Generator
from fastapi import FastAPI
from sqlalchemy.orm import Session

from src.logger import logger
from src.routers import tasks_router
from src.database import SessionLocal

logger.info("Task manager started")

app = FastAPI(title="Task Manager API")

app.include_router(tasks_router)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session for one request.

    Opens a session before the route runs and closes it afterward, so
    connections are not leaked.

    Yields:
        Session: Database session bound to this request.

    Example:
        Injected via ``Depends(get_db)`` on route parameters.
    """
    logger.info("Getting db")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    """
    Root endpoint used as a simple liveness check.

    Returns:
        str: Static message confirming the API process is up.

    Note:
        Does not verify database connectivity; use a dedicated health
        route if you need that.
    """
    logger.info("Getting root")
    return {"message": "Task Manager API is running"}
