from fastapi import FastAPI

from src.database import Base, engine
from src.logger import logger
from src.routers import tasks_router, projects_router

Base.metadata.create_all(bind=engine)

logger.info("Task manager started")

app = FastAPI(title="Task Manager API")

app.include_router(tasks_router)
app.include_router(projects_router)


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    """
    Root endpoint used as a simple liveness check.

    Returns:
        dict[str, str]: JSON with a ``message`` key.

    Note:
        Does not verify database connectivity; use a dedicated health
        route if you need that.
    """
    logger.info("Getting root")
    return {"message": "Task Manager API is running"}
