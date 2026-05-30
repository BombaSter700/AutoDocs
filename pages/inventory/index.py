from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget

from database import (
    InventoryCheck,
    InventoryCheckItem,
    InventoryCheckCreate,
    InventoryCheckItemCreate,
)


class InventoryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Инвентаризация")

        layout = QVBoxLayout(self)

        title = QLabel("Инвентаризация")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(self._create_list_tab(), "Проверки")
        tabs.addTab(self._create_add_tab(), "Новая проверка")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Список инвентаризаций (в разработке)"))
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Форма инвентаризации (в разработке)"))
        return w
