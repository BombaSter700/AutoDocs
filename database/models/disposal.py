from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..base import Base


class WriteOffAct(Base):
    __tablename__ = "write_off_acts"

    id = Column(Integer, primary_key=True)
    act_number = Column(
        String(100), nullable=False, comment="Номер акта"
    )
    act_date = Column(Date, nullable=False, comment="Дата составления")
    reason = Column(Text, nullable=False, comment="Причина списания")
    decision = Column(Text, comment="Решение комиссии / заключение")

    status = Column(
        String(50),
        nullable=False,
        default="pending",
        comment="Статус: pending, approved, completed",
    )
    commission_members = Column(
        Text, comment="Члены комиссии (ФИО через запятую)"
    )

    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    document_id = Column(
        Integer, ForeignKey("documents.id"), comment="Сопроводительный документ"
    )

    equipment = relationship("Equipment", back_populates="write_off_acts")
    document = relationship("Document", back_populates="write_off_acts")
