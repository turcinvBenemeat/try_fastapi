from typing import Optional

from pydantic import BaseModel, ConfigDict

# Data needed to CREATE a task (sent by user)
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


# This is used for creating a new task
class TaskCreate(TaskBase):
    pass


# Data sent BACK to the user (includes the database ID)
class Task(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
