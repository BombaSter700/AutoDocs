from datetime import date

from .base import _BaseSchema


class WriteOffActCreate(_BaseSchema):
    act_number: str
    act_date: date
    reason: str
    decision: str | None = None
    status: str = "pending"
    commission_members: str | None = None
    equipment_id: int
    document_id: int | None = None


class WriteOffActRead(WriteOffActCreate):
    id: int
