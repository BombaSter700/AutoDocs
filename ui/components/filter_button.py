from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import ComboBox, SearchLineEdit, DateEdit, PushButton, BodyLabel


class EventsFilter(QWidget):
    filter_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        filter_layout = QHBoxLayout()

        filter_layout.addWidget(BodyLabel("Статус:"))
        self.status_filter = ComboBox()
        self.status_filter.addItem("Все статусы", "")
        self.status_filter.addItem("Запланировано", "planned")
        self.status_filter.addItem("В процессе", "in_progress")
        self.status_filter.addItem("Завершено", "completed")
        self.status_filter.addItem("Отменено", "cancelled")
        self.status_filter.addItem("Отложено", "postponed")
        self.status_filter.currentIndexChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.status_filter)

        filter_layout.addWidget(BodyLabel("Поиск:"))
        self.search_input = SearchLineEdit()
        self.search_input.setPlaceholderText("По описанию или типу...")
        self.search_input.setMaximumWidth(200)
        self.search_input.textChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.search_input)

        filter_layout.addWidget(BodyLabel("С:"))
        self.date_from = DateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.dateChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.date_from)

        filter_layout.addWidget(BodyLabel("По:"))
        self.date_to = DateEdit()
        self.date_to.setDate(QDate.currentDate().addDays(30))
        self.date_to.dateChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.date_to)

        self.reset_btn = PushButton("Сбросить")
        self.reset_btn.clicked.connect(self.reset_filters)
        filter_layout.addWidget(self.reset_btn)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)

    def _on_filter_changed(self):
        self.filter_changed.emit()

    def reset_filters(self):
        self.status_filter.setCurrentIndex(0)
        self.search_input.clear()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_to.setDate(QDate.currentDate().addDays(30))

    def get_filters(self):
        return {
            "status": self.status_filter.currentData(),
            "search_term": self.search_input.text().strip(),
            "date_from": self.date_from.date().toString("yyyy-MM-dd"),
            "date_to": self.date_to.date().toString("yyyy-MM-dd"),
        }
