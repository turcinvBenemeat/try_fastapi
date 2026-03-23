from pydantic import BaseModel
from typing import Optional

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

    # This part is crucial for SQLAlchemy compatibility!
    class Config:
        from_attributes = True