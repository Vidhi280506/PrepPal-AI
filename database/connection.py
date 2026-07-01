"""
PrepPal AI — Database Connection & Session Management
SQLAlchemy 2.0 engine setup for SQLite with async support.
"""
import os
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from models.db_models import Base
from utils.logger import logger

# ── Database path ────────────────────────────────────────────────────────────
_db_url = os.getenv("DATABASE_URL", "sqlite:///./data/preppal.db")

# Ensure the data directory exists
_db_path = _db_url.replace("sqlite:///", "").replace("sqlite://", "")
if _db_path and not _db_path.startswith(":"):
    Path(_db_path).parent.mkdir(parents=True, exist_ok=True)

# ── Engine ──────────────────────────────────────────────────────────────────
engine = create_engine(
    _db_url,
    connect_args={"check_same_thread": False},  # needed for SQLite + threading
    echo=os.getenv("DEBUG", "false").lower() == "true",
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable WAL mode and foreign keys for SQLite."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# ── Session factory ──────────────────────────────────────────────────────────
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    FastAPI dependency: yields a database session and ensures it is closed.
    Usage:
        @router.get(...)
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Create all tables if they do not exist.
    Called once at application startup.
    """
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema ready.")
