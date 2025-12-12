from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

# Import our new modules
import models
import schemas
from database import engine, get_db

# Create the database tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Professional To-Do API")

# --- ENDPOINTS ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do API! Go to /docs to use it."}

@app.post("/todos/", response_model=schemas.TodoResponse)
async def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.TodoDB(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[schemas.TodoResponse])
async def get_todos(completed: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(models.TodoDB)
    if completed is not None:
        query = query.filter(models.TodoDB.is_completed == completed)
    return query.all()

@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.patch("/todos/{todo_id}/complete", response_model=schemas.TodoResponse)
async def mark_complete(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.is_completed = True
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"} 