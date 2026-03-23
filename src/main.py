from ansible.playbook import task
from fastapi import FastAPI, HTTPException
from schemas import Task

app = FastAPI(title="Task Manager API")

# Temporary in-memory database
tasks = []

@app.get("/")
def root():
    """
    Root endpoint
    :return: Message that Task Manager is running
    """
    return {"message": "Task Manager is running"}

@app.get("/tasks")
def get_tasks():
    """
    Returns a list of all tasks
    :return: The list of tasks
    """
    return tasks

@app.get("/tasks/{task}")
def get_task(task_id: int):
    """
    Returns a single task
    :param task_id: Id of the task
    :return: The task or the error message
    """
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def create_task(task: Task):
    """
    Create a new task
    :param task: Task to create
    :return: The created task
    """
    tasks.append(task)
    return task