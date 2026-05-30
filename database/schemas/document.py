from datetime import date

from .base import _BaseSchema


class DocumentCreate(_BaseSchema):
    doc_type: str
    doc_number: str | None = None
    doc_date: date | None = None
    title: str
    file_path: str | None = None
    status: str = "draft"
    notes: str | None = None
    created_by_id: int | None = None
    approved_by_id: int | None = None
    approved_date: date | None = None
    equipment_id: int | None = None
    location_id: int | None = None


class DocumentRead(DocumentCreate):
    id: int
