from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import TabWidget, TitleLabel, BodyLabel

from database import InventoryCheck, InventoryCheckItem
from utillities.useTables import DataTableWidget


class InventoryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Инвентаризация")

        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("Инвентаризация"))

        tabs = TabWidget(self)
        tabs.addTab(self._create_list_tab(), "Проверки")
        tabs.addTab(self._create_items_tab(), "Позиции")
        tabs.addTab(self._create_add_tab(), "Новая проверка")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        columns = [
            ("Дата начала", "started_at", 150),
            ("Дата завершения", "finished_at", 150),
            ("Статус", "status", 100),
            ("Локация", "location.name", 180),
            ("Ответственный", "performed_by.full_name", 180),
            ("Заключение", "summary", 250),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table = DataTableWidget(InventoryCheck, columns)
        layout.addWidget(self.table)
        return w

    def _create_items_tab(self) -> QWidget:
        columns = [
            ("Проверка", "check.id", 80),
            ("Оборудование", "equipment.name", 220),
            ("Ожидаемый статус", "expected_status", 130),
            ("Фактический статус", "actual_status", 130),
            ("Факт. локация", "actual_location.name", 180),
            ("Комментарий", "comment", 200),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table_items = DataTableWidget(InventoryCheckItem, columns)
        layout.addWidget(self.table_items)
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(BodyLabel("Форма инвентаризации (в разработке)"))
        return w
