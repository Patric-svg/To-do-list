from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    due_date = Column(Date)
    is_completed = Column(Boolean, default=False)