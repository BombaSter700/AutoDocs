"""
Generic base repository providing CRUD operations over SQLAlchemy sessions.

Usage example
-------------
from config import get_session
from database import Employee
from database.repository import BaseRepository

with get_session() as session:
    repo = BaseRepository(session, Employee)
    employees = repo.get_all()
"""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from .base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Thin wrapper around a SQLAlchemy Session that provides
    generic get / add / delete helpers for any ORM model.

    Domain-specific repositories should subclass this and add
    query methods as needed.
    """

    def __init__(self, session: Session, model: Type[T]) -> None:
        self._session = session
        self._model = model

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_all(self) -> List[T]:
        return self._session.query(self._model).all()

    def get_by_id(self, record_id: int) -> Optional[T]:
        return self._session.get(self._model, record_id)

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def add(self, obj: T) -> T:
        """Persist a new ORM instance and flush so its id is populated."""
        self._session.add(obj)
        self._session.flush()
        return obj

    def update(self, obj: T) -> T:
        """Merge a detached or modified instance back into the session."""
        merged = self._session.merge(obj)
        self._session.flush()
        return merged

    def delete(self, record_id: int) -> bool:
        """Delete by primary key. Returns False if the record was not found."""
        obj = self.get_by_id(record_id)
        if obj is None:
            return False
        self._session.delete(obj)
        return True
