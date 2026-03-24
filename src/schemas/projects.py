from typing import Optional

from pydantic import BaseModel, ConfigDict

# TODO: Update structure

# Data needed to CREATE a task (sent by user)
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


# This is used for creating a new task
class TaskCreate(ProjectBase):
    pass


# Data sent BACK to the user (includes the database ID)
class Task(ProjectBase):
    id: int

    model_config = ConfigDict(from_attributes=True)