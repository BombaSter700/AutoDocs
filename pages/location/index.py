from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import TabWidget, TitleLabel, BodyLabel

from database import Location
from utillities.useTables import DataTableWidget


class LocationPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Локации")

        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("Локации / Помещения"))

        tabs = TabWidget(self)
        tabs.addTab(self._create_list_tab(), "Список")
        tabs.addTab(self._create_add_tab(), "Добавить")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        columns = [
            ("Название", "name", 250),
            ("Здание", "building", 140),
            ("Этаж", "floor", 60),
            ("Кабинет", "room", 100),
            ("Тип", "location_type", 120),
            ("Примечания", "notes", 200),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table = DataTableWidget(Location, columns)
        layout.addWidget(self.table)
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(BodyLabel("Форма добавления локации (в разработке)"))
        return w
