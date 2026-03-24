"""ORM model for the ``tasks`` table."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Task(Base):
    """
    A task row; optionally linked to a :class:`~src.models.projects.Project`.

    Attributes:
        id: Primary key.
        title: Short title.
        description: Optional longer text.
        completed: Whether the task is done.
        created_at: Row creation timestamp.
        updated_at: Last update timestamp (set on change when using ORM updates).
        project_id: Optional FK to ``projects.id``.
        project: Parent ``Project`` instance when loaded via relationship.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = relationship("Project", back_populates="tasks")
