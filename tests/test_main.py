"""API tests via ``TestClient``; fixtures: ``client``, ``db_session`` (``conftest.py``)."""

def test_read_root(client, db_session) -> None:
    """``GET /`` → 200 and ``{"message": ...}``."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API is running"}


def test_get_tasks(client, db_session) -> None:
    """Two ``POST /tasks``, then ``GET /tasks`` → list of length 2."""
    client.post("/tasks", json={
        "title": "Task 1",
        "description": "Description 1",
        "completed": False,
    })
    client.post("/tasks", json={
        "title": "Task 2",
        "description": "Description 2",
        "completed": True,
    })

    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2


def test_create_task(client, db_session) -> None:
    """``POST /tasks`` → 200, ``id`` int, fields echo payload."""
    payload = {
        "title": "Testing Task",
        "description": "Task Description",
        "completed": False,
    }
    response = client.post("/tasks", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["title"] == "Testing Task"
    assert data["description"] == "Task Description"
    assert data["completed"] is False


def test_get_task(client, db_session) -> None:
    """Create task; ``GET /tasks/{id}`` JSON equals create response."""
    payload = {
        "title": "Testing Task",
        "description": "Task Description",
        "completed": False,
    }

    create_response = client.post("/tasks", json=payload)
    task = create_response.json()

    response = client.get(f"/tasks/{task['id']}")

    assert response.status_code == 200
    data = response.json()

    assert data == task


def test_get_task_not_found(client, db_session) -> None:
    """Missing id → 404 and ``{"detail": "Task not found"}``."""
    response = client.get("/tasks/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task(client, db_session) -> None:
    """``PUT /tasks/{id}`` returns updated title, description, completed."""
    create_response = client.post("/tasks", json={
        "title": "Old",
        "description": "Old description",
        "completed": False,
    })

    task = create_response.json()

    update_payload = {
        "title": "New",
        "description": "New description",
        "completed": True,
    }

    response = client.put(f"/tasks/{task['id']}", json=update_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "New"
    assert data["description"] == "New description"
    assert data["completed"] is True


def test_delete_task(client, db_session) -> None:
    """``DELETE /tasks/{id}`` (200 or 204); subsequent GET → 404."""
    create_response = client.post("/tasks", json={
        "title": "Delete me",
        "description": "Soon gone",
        "completed": False,
    })

    task = create_response.json()

    response = client.delete(f"/tasks/{task['id']}")
    assert response.status_code in (200, 204)

    check = client.get(f"/tasks/{task['id']}")
    assert check.status_code == 404
