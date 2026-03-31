# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings   # still import settings, but don't use it yet

Base = declarative_base()

# Do NOT create engine here at module level
_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(settings.database_url, pool_pre_ping=True)  # pool_pre_ping helps with Docker restarts
    return _engine

def get_db():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Remove the top-level create_all() from main.py