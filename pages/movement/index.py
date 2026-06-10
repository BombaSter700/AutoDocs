from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import TabWidget, TitleLabel, BodyLabel

from database import EquipmentMovement
from utillities.useTables import DataTableWidget


class MovementPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Перемещения")

        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("Перемещения оборудования"))

        tabs = TabWidget(self)
        tabs.addTab(self._create_list_tab(), "История")
        tabs.addTab(self._create_add_tab(), "Новое перемещение")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        columns = [
            ("Дата", "moved_at", 150),
            ("Оборудование", "equipment.name", 220),
            ("Откуда", "from_location.name", 180),
            ("Куда", "to_location.name", 180),
            ("Кто переместил", "moved_by.full_name", 180),
            ("Основание", "document.title", 200),
            ("Причина", "reason", 200),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table = DataTableWidget(EquipmentMovement, columns)
        layout.addWidget(self.table)
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(BodyLabel("Форма перемещения (в разработке)"))
        return w
