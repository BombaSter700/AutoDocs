from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget

from database import (
    MaintenanceRecord,
    MaintenanceRecordCreate,
    MaintenanceRecordRead,
)


class MaintenancePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Обслуживание")

        layout = QVBoxLayout(self)

        title = QLabel("Техническое обслуживание")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(self._create_list_tab(), "История")
        tabs.addTab(self._create_add_tab(), "Новая запись")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("История обслуживания (в разработке)"))
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Форма записи обслуживания (в разработке)"))
        return w
