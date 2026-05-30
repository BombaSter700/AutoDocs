from datetime import date

from .base import _BaseSchema


class LocationCreate(_BaseSchema):
    name: str
    building: str | None = None
    floor: int | None = None
    room: str | None = None
    location_type: str = "room"
    notes: str | None = None


class LocationRead(LocationCreate):
    id: int


class EmployeeCreate(_BaseSchema):
    full_name: str
    position: str | None = None
    department: str | None = None
    employee_number: str | None = None
    phone: str | None = None
    email: str | None = None
    hire_date: date | None = None
    is_active: int = 1
    notes: str | None = None


class EmployeeRead(EmployeeCreate):
    id: int
