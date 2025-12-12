from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. The Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# 2. The Engine (The core connection)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. The Session Maker (Creates database sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Base Class (All models will inherit from this)
Base = declarative_base()

# 5. Dependency (The "get_db" function we discussed)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()