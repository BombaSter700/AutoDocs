from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from ..base import Base


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True)
    maintenance_type = Column(
        String(50),
        nullable=False,
        comment="Тип: diagnostic, repair, preventive, upgrade, cleaning",
    )
    status = Column(
        String(50),
        nullable=False,
        default="planned",
        comment="Статус: planned, in_progress, completed, cancelled",
    )
    description = Column(Text, comment="Описание работ")
    performed_at = Column(DateTime, comment="Дата проведения")
    next_due_at = Column(DateTime, comment="Следующее плановое обслуживание")
    executor = Column(
        String(200), comment="Исполнитель (ФИО или организация)"
    )
    cost = Column(Numeric(12, 2), default=0, comment="Стоимость")
    result = Column(Text, comment="Результат / заключение")

    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    document_id = Column(
        Integer, ForeignKey("documents.id"), comment="Акт выполненных работ"
    )

    equipment = relationship("Equipment", back_populates="maintenance_records")
    document = relationship("Document", back_populates="maintenance_records")
