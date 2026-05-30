from datetime import datetime

from .base import _BaseSchema


class EquipmentMovementCreate(_BaseSchema):
    moved_at: datetime
    reason: str | None = None
    equipment_id: int
    from_location_id: int | None = None
    to_location_id: int | None = None
    moved_by_id: int | None = None
    document_id: int | None = None


class EquipmentMovementRead(EquipmentMovementCreate):
    id: int
