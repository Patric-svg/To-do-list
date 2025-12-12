from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from uuid import UUID, uuid4

# Initialize the app with a professional title and version
app = FastAPI(
    title="Professional To-Do API",
    description="A robust API for managing tasks.",
    version="1.0.0"
)

# --- MODELS ---

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, example="Buy Groceries")
    description: Optional[str] = Field(None, max_length=300, example="Milk, Eggs, Bread")
    due_date: date

class Todo(TodoCreate):
    id: UUID
    is_completed: bool = False

# --- DATABASE (In-Memory) ---
todo_list: List[Todo] = []

# --- ENDPOINTS ---

@app.get("/")
async def root():
    """A simple welcome message to verify the API is running."""
    return {"message": "Welcome to your To-Do API. Go to /docs for the interface."}

@app.post("/todos/", response_model=Todo, status_code=201, summary="Create a Task")
async def create_todo(todo_in: TodoCreate):
    """
    Create a new to-do item with a title, description, and due date.
    """
    new_todo = Todo(
        id=uuid4(),
        title=todo_in.title,
        description=todo_in.description,
        due_date=todo_in.due_date,
        is_completed=False
    )
    todo_list.append(new_todo)
    return new_todo

@app.get("/todos/", response_model=List[Todo], summary="List all Tasks")
async def get_todos(completed: Optional[bool] = Query(None, description="Filter by status")):
    """
    Get a list of all tasks. Optionally filter by 'completed' status.
    """
    if completed is None:
        return todo_list
    return [t for t in todo_list if t.is_completed == completed]

@app.get("/todos/{todo_id}", response_model=Todo, summary="Get one Task")
async def get_todo_by_id(todo_id: UUID):
    for todo in todo_list:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.patch("/todos/{todo_id}/complete", response_model=Todo, summary="Mark as Complete")
async def mark_complete(todo_id: UUID):
    for todo in todo_list:
        if todo.id == todo_id:
            todo.is_completed = True
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", summary="Delete a Task")
async def delete_todo(todo_id: UUID):
    for i, todo in enumerate(todo_list):
        if todo.id == todo_id:
            del todo_list[i]
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")