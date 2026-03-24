from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db
from src.logger import logger
from src.models.tasks import Task as TaskORM
from src.schemas.tasks import Task as TaskSchema, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskSchema])
def get_tasks(db: Session = Depends(get_db)) -> list[TaskORM]:
    """List all tasks."""
    logger.info("Getting all tasks")
    return list(db.scalars(select(TaskORM)).all())


@router.get("/{task_id}", response_model=TaskSchema)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskORM:
    """Get one task by id."""
    logger.info(f"Getting task with ID {task_id}")
    task = db.scalars(select(TaskORM).where(TaskORM.id == task_id)).first()
    if not task:
        logger.error(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskSchema)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)) -> TaskORM:
    """Create a task."""
    logger.info("Creating new task")
    new_task = TaskORM(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        project_id=task_data.project_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    logger.info(f"Created new task with ID {new_task.id}")
    return new_task


@router.put("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskORM:
    """Update a task."""
    logger.info(f"Updating task with ID {task_id}")
    task = db.scalars(select(TaskORM).where(TaskORM.id == task_id)).first()
    if not task:
        logger.error(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    task.project_id = task_data.project_id
    db.commit()
    db.refresh(task)
    logger.info(f"Task with ID {task_id} updated")
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """Delete a task."""
    logger.info(f"Deleting task with ID {task_id}")
    task = db.scalars(select(TaskORM).where(TaskORM.id == task_id)).first()
    if not task:
        logger.error(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    logger.info(f"Task with ID {task_id} deleted")
    return {"message": f"Task {task_id} was deleted"}
