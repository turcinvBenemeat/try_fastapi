from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    """Shared fields for create/update (writable ORM columns only)."""

    name: str
    description: Optional[str] = None
    # ORM default is True; keep the same so “omit field” semantics match the DB.
    is_active: bool = True


class ProjectCreate(ProjectBase):
    """Body for ``POST /projects`` (when implemented with persistence)."""

    pass


class Project(ProjectBase):
    """API representation of a row; aligns with ``src.models.projects.Project``."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
