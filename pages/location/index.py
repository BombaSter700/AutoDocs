from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget

from database import Location, LocationCreate, LocationRead


class LocationPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Локации")

        layout = QVBoxLayout(self)

        title = QLabel("Локации / Помещения")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(self._create_list_tab(), "Список")
        tabs.addTab(self._create_add_tab(), "Добавить")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Таблица локаций (в разработке)"))
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Форма добавления локации (в разработке)"))
        return w
