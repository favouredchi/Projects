# Create a to_do list application that allows users to create, read, update, and delete tasks

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()

# Database Setup
DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class Task(Base):
       __tablename__ = "tasks"
       id = Column(Integer, primary_key=True, index=True)
       title = Column(String, index=True)
       description = Column(String, nullable=True)
       completed = Column(Boolean, default=False)

# Create Database
Base.metadata.create_all(bind=engine)

# Pydantic Schema
class TaskCreate(BaseModel):
    title: str
    description: str = None

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Return a list of tasks
@app.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# Return a single task
@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return

# Create a new task
@app.post("/tasks/")
def create_task(title: str, content: str, db: Session = Depends(get_db)):
    task = Task(title=title, content=content)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# Update a single task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str, content: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = title
    task.content = content
    db.commit()
    db.refresh(task)
    return task

# Delete a single task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return

# Define a Task model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)



