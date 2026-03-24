def test_read_root(client, db_session) -> None:
    """
    Ensure ``GET /`` behaves as the API liveness/root response.

    Verifies HTTP 200 and that the JSON body matches the root handler’s
    ``{"message": ...}`` payload so clients can detect a healthy server
    without touching the database.
    """
    
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API is running"}

def test_create_task(client, db_session) -> None:
    """
    Ensure ``POST /tasks`` persists a task and returns it with a server-assigned id.

    Sends a body matching ``TaskCreate`` (title, description, completed), then
    asserts the response is successful, includes an integer ``id``, and echoes
    the submitted fields. Expects ``id == 1`` when the task table is empty (first
    row); if other tests insert tasks first, this assertion may need isolation
    (e.g. transactional DB or id checks without a fixed value).
    """
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
    assert data["id"] == 1
    assert data["title"] == "Testing Task"
    assert data["description"] == "Task Description"
    assert data["completed"] is False

