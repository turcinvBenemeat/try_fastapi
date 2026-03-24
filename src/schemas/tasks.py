from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    """Shared fields for create/update payloads (matches writable ORM columns)."""

    title: str
    description: Optional[str] = None
    completed: bool = False
    project_id: Optional[int] = None


class TaskCreate(TaskBase):
    """Body for ``POST /tasks`` (no ``id`` or timestamps; server sets those)."""

    pass


class Task(TaskBase):
    """API representation of a row; aligns with ``src.models.tasks.Task``."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
