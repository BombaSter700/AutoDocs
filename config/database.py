import os
from contextlib import contextmanager
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from database import Base

load_dotenv()


def _get_db_path() -> str:
    """Return path to the SQLite database file.

    Priority:
    1. DB_PATH env var (absolute path)
    2. ./inventory.db in the current working directory
    """
    env_path = os.getenv("DB_PATH")
    if env_path:
        return env_path
    return os.path.join(os.getcwd(), "inventory.db")


def _build_url() -> str:
    return f"sqlite:///{_get_db_path()}"


# Enable WAL mode + foreign keys for better concurrency
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


engine = create_engine(
    _build_url(),
    echo=False,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager that provides a transactional DB session."""
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()