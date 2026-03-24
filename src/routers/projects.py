from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db
from src.logger import logger
from src.models.projects import Project as ProjectORM
from src.schemas.projects import Project as ProjectSchema, ProjectCreate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectSchema])
def get_projects(db: Session = Depends(get_db)) -> list[ProjectORM]:
    """List all projects."""
    logger.info("Getting all projects")
    return list(db.scalars(select(ProjectORM)).all())


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectORM:
    """Get one project by id."""
    logger.info(f"Getting project with ID {project_id}")
    project = db.scalars(select(ProjectORM).where(ProjectORM.id == project_id)).first()
    if not project:
        logger.error(f"Project with ID {project_id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectSchema)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
) -> ProjectORM:
    """Create a project."""
    logger.info("Creating new project")
    new_project = ProjectORM(
        name=project_data.name,
        description=project_data.description,
        is_active=project_data.is_active,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    logger.info(f"Created new project with ID {new_project.id}")
    return new_project


@router.put("/{project_id}", response_model=ProjectSchema)
def update_project(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
) -> ProjectORM:
    """Update a project."""
    logger.info(f"Updating project with ID {project_id}")
    project = db.scalars(select(ProjectORM).where(ProjectORM.id == project_id)).first()
    if not project:
        logger.error(f"Project with ID {project_id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = project_data.name
    project.description = project_data.description
    project.is_active = project_data.is_active
    db.commit()
    db.refresh(project)
    logger.info(f"Project with ID {project_id} updated")
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """Delete a project."""
    logger.info(f"Deleting project with ID {project_id}")
    project = db.scalars(select(ProjectORM).where(ProjectORM.id == project_id)).first()
    if not project:
        logger.error(f"Project with ID {project_id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    logger.info(f"Project with ID {project_id} deleted")
    return {"message": f"Project {project_id} was deleted"}
