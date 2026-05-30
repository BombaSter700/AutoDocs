from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from ..base import Base


class EquipmentMovement(Base):
    __tablename__ = "equipment_movements"

    id = Column(Integer, primary_key=True)
    moved_at = Column(
        DateTime, nullable=False, comment="Дата и время перемещения"
    )
    reason = Column(Text, comment="Причина перемещения")

    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    from_location_id = Column(
        Integer, ForeignKey("locations.id"), comment="Откуда"
    )
    to_location_id = Column(
        Integer, ForeignKey("locations.id"), comment="Куда"
    )
    moved_by_id = Column(
        Integer, ForeignKey("employees.id"), comment="Кто переместил"
    )
    document_id = Column(
        Integer, ForeignKey("documents.id"), comment="Основание (документ)"
    )

    equipment = relationship("Equipment", back_populates="movements")
    moved_by = relationship("Employee", back_populates="movements")
    document = relationship("Document", back_populates="movements")
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location = relationship("Location", foreign_keys=[to_location_id])
