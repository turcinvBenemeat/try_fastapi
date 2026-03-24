"""ORM model for the ``projects`` table."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Project(Base):
    """
    A project grouping related :class:`~src.models.tasks.Task` rows.

    Attributes:
        id: Primary key.
        name: Display name.
        description: Optional details.
        created_at: Row creation timestamp.
        updated_at: Last update timestamp (set on change when using ORM updates).
        is_active: Soft-enable flag for the project.
        tasks: Child tasks; ``cascade`` removes orphans when a project is deleted
            (ORM-level; ensure migrations match your DB policy).
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
    )
