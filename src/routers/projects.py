from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session


from src.database import get_db
from src.models.projects import Project as ProjectORM
from src.schemas.projects import Project as ProjectSchema, ProjectCreate
from src.logger import logger

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectSchema])
def get_projects(db: Session = Depends(get_db)) -> list[ProjectORM]:
    """Placeholder: list all projects."""
    logger.info("Get all projects")
    return list(db.scalars(select(ProjectORM)).all())


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectORM:
    """Placeholder: single project by id."""
    logger.info(f"Getting project with ID: {project_id}")
    project = db.scalars(select(ProjectORM).where(ProjectORM.id == project_id)).first()
    if not project:
        logger.error(f"Project with ID: {project_id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectSchema)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)) -> ProjectORM:
    """Placeholder: create project (body echoed only)."""
    logger.info("Creating new project")
    new_project = ProjectORM(...)
    ... # TODO
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    logger.info(f"Project with ID: {new_project.id} created")
    return new_project


@router.put("/{project_id}")
def update_project(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
) -> ProjectORM:
    """Placeholder: update project."""
    logger.info(f"Updating project with ID {project_id}")
    project = db.scalars(select(ProjectORM).where(ProjectORM.id == project_id)).first()
    if not project:
        logger.error(f"Project with ID: {project_id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    ... # TODO
    db.commit()
    db.refresh(project)
    logger.info(f"Project with ID {project.id} updated")
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Placeholder: delete project."""
    logger.info(f"Deleting project with ID {project_id}")
    project = db.scalars(select(ProjectORM).where(ProjectORM.id == project_id)).first()
    if not project:
        logger.error(f"Project with ID: {project_id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    logger.info(f"Project with ID {project.id} deleted")
    return {"message": f"Project with ID {project.id} was deleted"}
