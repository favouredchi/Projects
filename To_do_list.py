# Create a to_do list application that allows users to create, read, update, and delete tasks.

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the table
Base.metadata.create_all(bind=engine)

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



