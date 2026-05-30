from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.orm import relationship

from ..base import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, comment="Название локации")
    building = Column(String(100), comment="Здание / корпус")
    floor = Column(Integer, comment="Этаж")
    room = Column(String(50), comment="Номер кабинета")
    location_type = Column(
        String(50),
        default="room",
        comment="Тип: classroom, office, lab, storage, server, other",
    )
    notes = Column(Text)

    equipment = relationship("Equipment", back_populates="location")
    documents = relationship("Document", back_populates="location")
    network_nodes = relationship("NetworkNode", back_populates="location")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(200), nullable=False)
    position = Column(String(150), comment="Должность")
    department = Column(String(150), comment="Отдел / подразделение")
    employee_number = Column(String(30), unique=True, comment="Табельный номер")
    phone = Column(String(30))
    email = Column(String(150))
    hire_date = Column(Date, comment="Дата приёма на работу")
    is_active = Column(
        Integer, nullable=False, default=1, comment="1 — активен, 0 — уволен"
    )
    notes = Column(Text)

    equipment = relationship("Equipment", back_populates="responsible_employee")
    documents = relationship(
        "Document",
        back_populates="created_by",
        foreign_keys="Document.created_by_id",
    )
    movements = relationship("EquipmentMovement", back_populates="moved_by")
    checks = relationship("InventoryCheck", back_populates="performed_by")
