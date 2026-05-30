from datetime import datetime

from .base import _BaseSchema


class InventoryCheckCreate(_BaseSchema):
    started_at: datetime
    finished_at: datetime | None = None
    status: str = "in_progress"
    summary: str | None = None
    location_id: int
    performed_by_id: int | None = None


class InventoryCheckRead(InventoryCheckCreate):
    id: int


class InventoryCheckItemCreate(_BaseSchema):
    expected_status: str | None = None
    actual_status: str | None = None
    comment: str | None = None
    check_id: int
    equipment_id: int
    actual_location_id: int | None = None


class InventoryCheckItemRead(InventoryCheckItemCreate):
    id: int
