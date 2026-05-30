from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..base import Base


class InventoryCheck(Base):
    __tablename__ = "inventory_checks"

    id = Column(Integer, primary_key=True)
    started_at = Column(
        DateTime, nullable=False, comment="Дата начала"
    )
    finished_at = Column(DateTime, comment="Дата завершения")
    status = Column(
        String(50),
        nullable=False,
        default="in_progress",
        comment="Статус: planned, in_progress, completed",
    )
    summary = Column(Text, comment="Итоговое заключение")

    location_id = Column(
        Integer, ForeignKey("locations.id"), nullable=False
    )
    performed_by_id = Column(
        Integer, ForeignKey("employees.id"), comment="Кто проводил"
    )

    location = relationship("Location")
    performed_by = relationship("Employee", back_populates="checks")
    items = relationship("InventoryCheckItem", back_populates="check")


class InventoryCheckItem(Base):
    __tablename__ = "inventory_check_items"

    id = Column(Integer, primary_key=True)
    expected_status = Column(
        String(50), comment="Ожидаемый статус по учёту"
    )
    actual_status = Column(String(50), comment="Фактический статус")
    comment = Column(Text, comment="Комментарий / расхождение")

    check_id = Column(
        Integer, ForeignKey("inventory_checks.id"), nullable=False
    )
    equipment_id = Column(
        Integer, ForeignKey("equipment.id"), nullable=False
    )
    actual_location_id = Column(
        Integer, ForeignKey("locations.id"), comment="Фактическое местоположение"
    )

    check = relationship("InventoryCheck", back_populates="items")
    equipment = relationship("Equipment", back_populates="check_items")
    actual_location = relationship("Location")
