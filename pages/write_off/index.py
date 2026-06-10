from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import TabWidget, TitleLabel, BodyLabel

from database import WriteOffAct
from utillities.useTables import DataTableWidget


class WriteOffPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Списание")

        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("Списание имущества"))

        tabs = TabWidget(self)
        tabs.addTab(self._create_list_tab(), "Акты")
        tabs.addTab(self._create_add_tab(), "Новый акт")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        columns = [
            ("Номер акта", "act_number", 120),
            ("Дата", "act_date", 100),
            ("Оборудование", "equipment.name", 220),
            ("Причина", "reason", 200),
            ("Статус", "status", 100),
            ("Решение", "decision", 200),
            ("Члены комиссии", "commission_members", 250),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table = DataTableWidget(WriteOffAct, columns)
        layout.addWidget(self.table)
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(BodyLabel("Форма акта списания (в разработке)"))
        return w
