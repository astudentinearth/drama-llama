from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import os
from config import settings

DATABASE_URL = settings.ai_database_url

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600, 
    echo=os.getenv("SQL_ECHO", "false").lower() == "true"
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@contextmanager
def get_db_context():
    """Context manager for non-FastAPI usage"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Initialize database (create all tables)
def init_db():
    from models.db_models import Base
    Base.metadata.create_all(bind=engine)

# Drop all tables (use carefully!)
def drop_db():
    from models.db_models import Base
    Base.metadata.drop_all(bind=engine)