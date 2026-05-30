from datetime import datetime
from decimal import Decimal

from .base import _BaseSchema


class MaintenanceRecordCreate(_BaseSchema):
    maintenance_type: str
    status: str = "planned"
    description: str | None = None
    performed_at: datetime | None = None
    next_due_at: datetime | None = None
    executor: str | None = None
    cost: Decimal = Decimal("0")
    result: str | None = None
    equipment_id: int
    document_id: int | None = None


class MaintenanceRecordRead(MaintenanceRecordCreate):
    id: int
