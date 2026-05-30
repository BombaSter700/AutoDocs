from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget

from database import EquipmentMovement, EquipmentMovementCreate, EquipmentMovementRead


class MovementPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Перемещения")

        layout = QVBoxLayout(self)

        title = QLabel("Перемещения оборудования")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(self._create_list_tab(), "История")
        tabs.addTab(self._create_add_tab(), "Новое перемещение")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("История перемещений (в разработке)"))
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Форма перемещения (в разработке)"))
        return w
