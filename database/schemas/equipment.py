from datetime import date
from decimal import Decimal

from .base import _BaseSchema


class EquipmentCreate(_BaseSchema):
    inventory_number: str
    name: str
    category: str | None = None
    model: str | None = None
    serial_number: str | None = None
    status: str = "in_use"
    supplier: str | None = None
    cost: Decimal | None = None
    purchase_date: date | None = None
    received_date: date | None = None
    commissioned_date: date | None = None
    warranty_until: date | None = None
    written_off_date: date | None = None
    notes: str | None = None
    location_id: int | None = None
    responsible_employee_id: int | None = None


class EquipmentRead(EquipmentCreate):
    id: int
