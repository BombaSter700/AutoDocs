from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import TabWidget, TitleLabel, BodyLabel

from database import Equipment
from utillities.useTables import DataTableWidget


class EquipmentPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Оборудование")

        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("Оборудование"))

        tabs = TabWidget(self)
        tabs.addTab(self._create_list_tab(), "Список")
        tabs.addTab(self._create_add_tab(), "Добавить")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        columns = [
            ("Инв. №", "inventory_number", 100),
            ("Наименование", "name", 250),
            ("Категория", "category", 120),
            ("Модель", "model", 140),
            ("Статус", "status", 120),
            ("Местоположение", "location.name", 180),
            ("Ответственный", "responsible_employee.full_name", 180),
            ("Дата покупки", "purchase_date", 100),
            ("Стоимость", "cost", 100),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table = DataTableWidget(Equipment, columns)
        layout.addWidget(self.table)
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(BodyLabel("Форма добавления оборудования (в разработке)"))
        return w
