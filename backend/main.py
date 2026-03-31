import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config import settings
# main.py — replace the old import
from database import get_db, Base, get_engine   # ← remove 'engine'
# Do NOT import 'engine' anymore
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoResponse

import time
from sqlalchemy.exc import OperationalError

def wait_for_db(engine, retries=100, delay=200):
    for i in range(retries):
        try:
            with engine.connect():
                print("DB is ready!")
                return
        except OperationalError:
            print(f"DB not ready, retry {i+1}/{retries}...")
            time.sleep(delay)
    raise Exception("Database not available")

# Base.metadata.create_all(bind=get_engine())

app = FastAPI(
    title="Todo API",
    description="API для управління списком задач",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/todos", response_model=list[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).order_by(Todo.created_at.desc()).all()


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/api/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.patch("/api/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.title is not None:
        db_todo.title = todo.title
    if todo.completed is not None:
        db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return None

@app.on_event("startup")
def startup():
    engine = get_engine()
    wait_for_db(engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
