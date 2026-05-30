from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from ..base import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    inventory_number = Column(
        String(50), nullable=False, unique=True, comment="Инвентарный номер"
    )

    name = Column(String(200), nullable=False, comment="Наименование")
    category = Column(String(100), comment="Категория (компьютер, принтер, МФУ, ...)")
    model = Column(String(150), comment="Модель")
    serial_number = Column(String(100), comment="Серийный номер (заводской)")

    status = Column(
        String(50),
        nullable=False,
        default="in_use",
        comment="Статус: received, in_use, under_maintenance, written_off, reserved",
    )

    supplier = Column(String(200), comment="Поставщик")
    cost = Column(Numeric(12, 2), comment="Стоимость при покупке")
    purchase_date = Column(Date, comment="Дата покупки")
    received_date = Column(Date, comment="Дата поступления в организацию")
    commissioned_date = Column(Date, comment="Дата ввода в эксплуатацию")
    warranty_until = Column(Date, comment="Гарантия до")
    written_off_date = Column(Date, comment="Дата списания")

    notes = Column(Text)

    location_id = Column(
        Integer, ForeignKey("locations.id"), comment="Текущее местоположение"
    )
    responsible_employee_id = Column(
        Integer, ForeignKey("employees.id"), comment="Материально-ответственное лицо"
    )

    location = relationship("Location", back_populates="equipment")
    responsible_employee = relationship("Employee", back_populates="equipment")
    documents = relationship("Document", back_populates="equipment")
    movements = relationship("EquipmentMovement", back_populates="equipment")
    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment")
    write_off_acts = relationship("WriteOffAct", back_populates="equipment")
    check_items = relationship("InventoryCheckItem", back_populates="equipment")
