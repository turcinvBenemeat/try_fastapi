"""Tests for ``src.main`` app wiring (e.g. root route not under ``/tasks``)."""

def test_read_root(client, db_session) -> None:
    """``GET /`` → 200 and ``{"message": ...}``."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API is running"}
