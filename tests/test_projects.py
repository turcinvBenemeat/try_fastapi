"""Tests for ``src.routers.projects`` (``/projects``)."""

def test_get_projects_empty(client, db_session) -> None:
    """``GET /projects`` → 200 and empty list when no rows."""
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json() == []


def test_get_projects_multiple(client, db_session) -> None:
    """Two ``POST /projects``, then ``GET /projects`` → list of length 2."""
    assert client.post("/projects", json={"name": "P1", "is_active": True}).status_code == 200
    assert client.post("/projects", json={"name": "P2", "is_active": False}).status_code == 200
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = {row["name"] for row in data}
    assert names == {"P1", "P2"}


def test_create_and_get_project(client, db_session) -> None:
    """``POST /projects`` then ``GET /projects/{id}`` returns the same JSON."""
    payload = {"name": "Alpha", "description": "First", "is_active": True}
    create = client.post("/projects", json=payload)
    assert create.status_code == 200
    project = create.json()
    assert project["name"] == "Alpha"
    assert project["description"] == "First"
    assert project["is_active"] is True
    assert "id" in project
    assert "created_at" in project
    assert "updated_at" in project

    get_one = client.get(f"/projects/{project['id']}")
    assert get_one.status_code == 200
    assert get_one.json() == project


def test_get_project_not_found(client, db_session) -> None:
    response = client.get("/projects/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_update_project(client, db_session) -> None:
    create = client.post("/projects", json={"name": "Old", "is_active": True})
    assert create.status_code == 200
    pid = create.json()["id"]

    response = client.put(
        f"/projects/{pid}",
        json={"name": "New", "description": "Updated", "is_active": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pid
    assert data["name"] == "New"
    assert data["description"] == "Updated"
    assert data["is_active"] is False


def test_delete_project(client, db_session) -> None:
    create = client.post("/projects", json={"name": "Gone", "is_active": True})
    assert create.status_code == 200
    pid = create.json()["id"]

    delete = client.delete(f"/projects/{pid}")
    assert delete.status_code == 200
    assert delete.json() == {"message": f"Project {pid} was deleted"}

    assert client.get(f"/projects/{pid}").status_code == 404
