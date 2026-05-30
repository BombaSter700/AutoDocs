from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    doc_type = Column(String(50), nullable=False, comment="Тип документа")
    doc_number = Column(String(100), comment="Номер документа")
    doc_date = Column(Date, comment="Дата документа")
    title = Column(String(255), nullable=False, comment="Заголовок / наименование")
    file_path = Column(String(500), comment="Путь к файлу на диске")

    status = Column(
        String(50),
        nullable=False,
        default="draft",
        comment="Статус: draft, active, approved, archived",
    )
    notes = Column(Text)

    created_by_id = Column(
        Integer, ForeignKey("employees.id"), comment="Кто создал"
    )
    approved_by_id = Column(
        Integer, ForeignKey("employees.id"), comment="Кто утвердил"
    )
    approved_date = Column(Date, comment="Дата утверждения")
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))

    created_by = relationship(
        "Employee", back_populates="documents", foreign_keys=[created_by_id]
    )
    approved_by = relationship("Employee", foreign_keys=[approved_by_id])
    equipment = relationship("Equipment", back_populates="documents")
    location = relationship("Location", back_populates="documents")
    movements = relationship("EquipmentMovement", back_populates="document")
    maintenance_records = relationship("MaintenanceRecord", back_populates="document")
    write_off_acts = relationship("WriteOffAct", back_populates="document")
