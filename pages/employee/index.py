from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import TabWidget, TitleLabel, BodyLabel

from database import Employee
from utillities.useTables import DataTableWidget


class EmployeePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Сотрудники")

        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("Сотрудники"))

        tabs = TabWidget(self)
        tabs.addTab(self._create_list_tab(), "Список")
        tabs.addTab(self._create_add_tab(), "Добавить")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        columns = [
            ("Таб. №", "employee_number", 80),
            ("ФИО", "full_name", 220),
            ("Должность", "position", 180),
            ("Отдел", "department", 160),
            ("Телефон", "phone", 140),
            ("Email", "email", 200),
            ("Дата приёма", "hire_date", 100),
            ("Активен", lambda e: "Да" if e.is_active else "Нет", 70),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table = DataTableWidget(Employee, columns)
        layout.addWidget(self.table)
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(BodyLabel("Форма добавления сотрудника (в разработке)"))
        return w
