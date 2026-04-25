"""Pydantic schemas for equipment, documents, and network accounting."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class _BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LocationCreate(_BaseSchema):
    name: str
    room: str | None = None
    notes: str | None = None


class LocationRead(LocationCreate):
    id: int


class EmployeeCreate(_BaseSchema):
    full_name: str
    position: str | None = None
    phone: str | None = None
    email: str | None = None
    is_active: int = 1


class EmployeeRead(EmployeeCreate):
    id: int


class EquipmentCreate(_BaseSchema):
    inventory_number: str
    name: str
    category: str | None = None
    model: str | None = None
    serial_number: str | None = None
    status: str = "in_use"
    purchase_date: date | None = None
    warranty_until: date | None = None
    notes: str | None = None
    location_id: int | None = None
    responsible_employee_id: int | None = None


class EquipmentRead(EquipmentCreate):
    id: int


class DocumentCreate(_BaseSchema):
    doc_type: str
    doc_number: str | None = None
    doc_date: date | None = None
    title: str
    file_path: str | None = None
    status: str = "draft"
    notes: str | None = None
    created_by_id: int | None = None
    equipment_id: int | None = None
    location_id: int | None = None


class DocumentRead(DocumentCreate):
    id: int


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


class MaintenanceRecordCreate(_BaseSchema):
    maintenance_type: str
    status: str = "planned"
    performed_at: datetime | None = None
    next_due_at: datetime | None = None
    executor: str | None = None
    cost: Decimal = Decimal("0")
    result: str | None = None
    equipment_id: int
    document_id: int | None = None


class MaintenanceRecordRead(MaintenanceRecordCreate):
    id: int


class WriteOffActCreate(_BaseSchema):
    act_number: str
    act_date: date
    reason: str
    decision: str | None = None
    equipment_id: int
    document_id: int | None = None


class WriteOffActRead(WriteOffActCreate):
    id: int


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
    actual_status: str | None = None
    comment: str | None = None
    check_id: int
    equipment_id: int
    actual_location_id: int | None = None


class InventoryCheckItemRead(InventoryCheckItemCreate):
    id: int


class NetworkNodeCreate(_BaseSchema):
    name: str
    node_type: str
    ip_address: str | None = None
    mac_address: str | None = None
    vendor: str | None = None
    model: str | None = None
    status: str = "active"
    notes: str | None = None
    location_id: int | None = None


class NetworkNodeRead(NetworkNodeCreate):
    id: int


class NetworkLinkCreate(_BaseSchema):
    port_from: str | None = None
    port_to: str | None = None
    link_type: str = "ethernet"
    status: str = "active"
    notes: str | None = None
    from_node_id: int
    to_node_id: int


class NetworkLinkRead(NetworkLinkCreate):
    id: int
