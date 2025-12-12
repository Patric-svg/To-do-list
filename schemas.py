from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Base schema (shared properties)
class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, example="Buy Groceries")
    description: Optional[str] = Field(None, max_length=300)
    due_date: date

# Schema for creating a Todo (same as base)
class TodoCreate(TodoBase):
    pass

# Schema for reading a Todo (adds ID and is_completed)
class TodoResponse(TodoBase):
    id: int
    is_completed: bool

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models