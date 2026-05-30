from .base import _BaseSchema
from .organization import LocationCreate, LocationRead, EmployeeCreate, EmployeeRead
from .equipment import EquipmentCreate, EquipmentRead
from .document import DocumentCreate, DocumentRead
from .movement import EquipmentMovementCreate, EquipmentMovementRead
from .maintenance import MaintenanceRecordCreate, MaintenanceRecordRead
from .disposal import WriteOffActCreate, WriteOffActRead
from .inventory import (
    InventoryCheckCreate,
    InventoryCheckRead,
    InventoryCheckItemCreate,
    InventoryCheckItemRead,
)
from .network import NetworkNodeCreate, NetworkNodeRead, NetworkLinkCreate, NetworkLinkRead

__all__ = [
    "_BaseSchema",
    "LocationCreate",
    "LocationRead",
    "EmployeeCreate",
    "EmployeeRead",
    "EquipmentCreate",
    "EquipmentRead",
    "DocumentCreate",
    "DocumentRead",
    "EquipmentMovementCreate",
    "EquipmentMovementRead",
    "MaintenanceRecordCreate",
    "MaintenanceRecordRead",
    "WriteOffActCreate",
    "WriteOffActRead",
    "InventoryCheckCreate",
    "InventoryCheckRead",
    "InventoryCheckItemCreate",
    "InventoryCheckItemRead",
    "NetworkNodeCreate",
    "NetworkNodeRead",
    "NetworkLinkCreate",
    "NetworkLinkRead",
]
