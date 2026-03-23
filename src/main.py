from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

# Import our database configuration and models
import models
import schemas
from database import engine, SessionLocal

# Create the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")


# Dependency to provide a database session for each request
def get_db():
    """
    Creates a new database session for a request and closes it
    after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Task Manager is running with persistent storage"}


@app.get("/tasks", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    """
    Retrieve all tasks from the database.
    """
    # query(models.Task) tells SQLAlchemy to fetch records from the 'tasks' table
    return db.query(models.Task).all()


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by its ID.
    """
    # .first() returns the first result or None if not found
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=schemas.Task)
def create_task(task_data: schemas.Task, db: Session = Depends(get_db)):
    """
    Create a new task record in the database.
    """
    # Create an instance of the SQLAlchemy model using data from the Pydantic schema
    new_task = models.Task(
        id=task_data.id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )

    db.add(new_task)  # Stage the new object in the session
    db.commit()  # Save changes to the .db file
    db.refresh(new_task)  # Refresh the object to get any DB-generated data
    return new_task