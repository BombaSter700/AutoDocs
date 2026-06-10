from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import TabWidget, TitleLabel, BodyLabel

from database import MaintenanceRecord
from utillities.useTables import DataTableWidget


class MaintenancePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Обслуживание")

        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("Техническое обслуживание"))

        tabs = TabWidget(self)
        tabs.addTab(self._create_list_tab(), "История")
        tabs.addTab(self._create_add_tab(), "Новая запись")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        columns = [
            ("Оборудование", "equipment.name", 220),
            ("Тип", "maintenance_type", 120),
            ("Статус", "status", 100),
            ("Описание", "description", 200),
            ("Дата проведения", "performed_at", 140),
            ("Следующее ТО", "next_due_at", 140),
            ("Исполнитель", "executor", 180),
            ("Стоимость", "cost", 100),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table = DataTableWidget(MaintenanceRecord, columns)
        layout.addWidget(self.table)
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(BodyLabel("Форма записи обслуживания (в разработке)"))
        return w
