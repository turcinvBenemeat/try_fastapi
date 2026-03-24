from typing import Any

from fastapi import APIRouter, Body

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def get_projects() -> list[dict[str, Any]]:
    """Placeholder: list all projects."""
    return []


@router.get("/{project_id}")
def get_project(project_id: int) -> dict[str, Any]:
    """Placeholder: single project by id."""
    return {"id": project_id, "name": "placeholder", "detail": "not implemented"}


@router.post("")
def create_project(
    data: dict[str, Any] | None = Body(default=None),
) -> dict[str, Any]:
    """Placeholder: create project (body echoed only)."""
    return {"id": 0, "placeholder": True, "echo": data or {}}


@router.put("/{project_id}")
def update_project(
    project_id: int,
    data: dict[str, Any] | None = Body(default=None),
) -> dict[str, Any]:
    """Placeholder: update project."""
    return {"id": project_id, "placeholder": True, "echo": data or {}}


@router.delete("/{project_id}")
def delete_project(project_id: int) -> dict[str, Any]:
    """Placeholder: delete project."""
    return {"id": project_id, "deleted": False, "message": "placeholder — no persistence"}
