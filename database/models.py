"""SQLAlchemy ORM models for equipment, documents, and network accounting."""

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    room = Column(String(50))
    notes = Column(Text)

    equipment = relationship("Equipment", back_populates="location")
    documents = relationship("Document", back_populates="location")
    network_nodes = relationship("NetworkNode", back_populates="location")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(200), nullable=False)
    position = Column(String(150))
    phone = Column(String(30))
    email = Column(String(150))
    is_active = Column(Integer, nullable=False, default=1)

    equipment = relationship("Equipment", back_populates="responsible_employee")
    documents = relationship("Document", back_populates="created_by")
    movements = relationship("EquipmentMovement", back_populates="moved_by")
    checks = relationship("InventoryCheck", back_populates="performed_by")


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    inventory_number = Column(String(50), nullable=False, unique=True)
    name = Column(String(150), nullable=False)
    category = Column(String(100))
    model = Column(String(150))
    serial_number = Column(String(100))
    status = Column(String(50), nullable=False, default="in_use")
    purchase_date = Column(Date)
    warranty_until = Column(Date)
    notes = Column(Text)

    location_id = Column(Integer, ForeignKey("locations.id"))
    responsible_employee_id = Column(Integer, ForeignKey("employees.id"))

    location = relationship("Location", back_populates="equipment")
    responsible_employee = relationship("Employee", back_populates="equipment")
    documents = relationship("Document", back_populates="equipment")
    movements = relationship("EquipmentMovement", back_populates="equipment")
    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment")
    write_off_acts = relationship("WriteOffAct", back_populates="equipment")
    check_items = relationship("InventoryCheckItem", back_populates="equipment")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    doc_type = Column(String(50), nullable=False)
    doc_number = Column(String(100))
    doc_date = Column(Date)
    title = Column(String(255), nullable=False)
    file_path = Column(String(500))
    status = Column(String(50), nullable=False, default="draft")
    notes = Column(Text)

    created_by_id = Column(Integer, ForeignKey("employees.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))

    created_by = relationship("Employee", back_populates="documents")
    equipment = relationship("Equipment", back_populates="documents")
    location = relationship("Location", back_populates="documents")
    movements = relationship("EquipmentMovement", back_populates="document")
    maintenance_records = relationship("MaintenanceRecord", back_populates="document")
    write_off_acts = relationship("WriteOffAct", back_populates="document")


class EquipmentMovement(Base):
    __tablename__ = "equipment_movements"

    id = Column(Integer, primary_key=True)
    moved_at = Column(DateTime, nullable=False)
    reason = Column(Text)

    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    from_location_id = Column(Integer, ForeignKey("locations.id"))
    to_location_id = Column(Integer, ForeignKey("locations.id"))
    moved_by_id = Column(Integer, ForeignKey("employees.id"))
    document_id = Column(Integer, ForeignKey("documents.id"))

    equipment = relationship("Equipment", back_populates="movements")
    moved_by = relationship("Employee", back_populates="movements")
    document = relationship("Document", back_populates="movements")
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location = relationship("Location", foreign_keys=[to_location_id])


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True)
    maintenance_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="planned")
    performed_at = Column(DateTime)
    next_due_at = Column(DateTime)
    executor = Column(String(200))
    cost = Column(Numeric(12, 2), default=0)
    result = Column(Text)

    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"))

    equipment = relationship("Equipment", back_populates="maintenance_records")
    document = relationship("Document", back_populates="maintenance_records")


class WriteOffAct(Base):
    __tablename__ = "write_off_acts"

    id = Column(Integer, primary_key=True)
    act_number = Column(String(100), nullable=False)
    act_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    decision = Column(Text)

    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"))

    equipment = relationship("Equipment", back_populates="write_off_acts")
    document = relationship("Document", back_populates="write_off_acts")


class InventoryCheck(Base):
    __tablename__ = "inventory_checks"

    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime)
    status = Column(String(50), nullable=False, default="in_progress")
    summary = Column(Text)

    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    performed_by_id = Column(Integer, ForeignKey("employees.id"))

    location = relationship("Location")
    performed_by = relationship("Employee", back_populates="checks")
    items = relationship("InventoryCheckItem", back_populates="check")


class InventoryCheckItem(Base):
    __tablename__ = "inventory_check_items"

    id = Column(Integer, primary_key=True)
    actual_status = Column(String(50))
    comment = Column(Text)

    check_id = Column(Integer, ForeignKey("inventory_checks.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    actual_location_id = Column(Integer, ForeignKey("locations.id"))

    check = relationship("InventoryCheck", back_populates="items")
    equipment = relationship("Equipment", back_populates="check_items")
    actual_location = relationship("Location")


class NetworkNode(Base):
    __tablename__ = "network_nodes"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    node_type = Column(String(50), nullable=False)
    ip_address = Column(String(45))
    mac_address = Column(String(32))
    vendor = Column(String(100))
    model = Column(String(150))
    status = Column(String(50), default="active")
    notes = Column(Text)

    location_id = Column(Integer, ForeignKey("locations.id"))

    location = relationship("Location", back_populates="network_nodes")
    outgoing_links = relationship(
        "NetworkLink", back_populates="from_node", foreign_keys="NetworkLink.from_node_id"
    )
    incoming_links = relationship(
        "NetworkLink", back_populates="to_node", foreign_keys="NetworkLink.to_node_id"
    )


class NetworkLink(Base):
    __tablename__ = "network_links"

    id = Column(Integer, primary_key=True)
    port_from = Column(String(50))
    port_to = Column(String(50))
    link_type = Column(String(50), default="ethernet")
    status = Column(String(50), default="active")
    notes = Column(Text)

    from_node_id = Column(Integer, ForeignKey("network_nodes.id"), nullable=False)
    to_node_id = Column(Integer, ForeignKey("network_nodes.id"), nullable=False)

    from_node = relationship("NetworkNode", back_populates="outgoing_links", foreign_keys=[from_node_id])
    to_node = relationship("NetworkNode", back_populates="incoming_links", foreign_keys=[to_node_id])
