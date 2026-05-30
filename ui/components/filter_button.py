from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt, QDate, pyqtSignal

class EventsFilter(QWidget):
    """Компонент фильтрации мероприятий"""
    
    #Флаг для переключения состояния поиска
    filter_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        filter_layout = QHBoxLayout() #протестировать, будет криво 
        
        filter_layout.addWidget(QLabel("Статус:"))
        self.status_filter = QComboBox()
        self.status_filter.addItem("Все статусы", "")
        self.status_filter.addItem("Запланировано", "planned")
        self.status_filter.addItem("🟡 В процессе", "in_progress")
        self.status_filter.addItem("🔵 Завершено", "completed")
        self.status_filter.addItem("🔴 Отменено", "cancelled")
        self.status_filter.addItem("🟠 Отложено", "postponed")
        self.status_filter.currentIndexChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.status_filter)

        # Поиск
        filter_layout.addWidget(QLabel("Поиск:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("По описанию или типу...")
        self.search_input.setMaximumWidth(200)
        self.search_input.textChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.search_input)

        # Диапазон дат
        filter_layout.addWidget(QLabel("С:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        self.date_from.dateChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.date_from)

        filter_layout.addWidget(QLabel("По:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate().addDays(30))
        self.date_to.setCalendarPopup(True)
        self.date_to.dateChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.date_to)

        # Кнопка сброса фильтров
        self.reset_btn = QPushButton("Сбросить")
        self.reset_btn.clicked.connect(self.reset_filters)
        filter_layout.addWidget(self.reset_btn)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
    def on_filter_changed(self):
        """Эмит сигнала при изменении фильтров"""
        self.filter_changed.emit()
        
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.status_filter.setCurrentIndex(0)
        self.search_input.clear()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_to.setDate(QDate.currentDate().addDays(30))
        
    def get_filters(self):
        """Получение текущих значений фильтров"""
        return {
            'status': self.status_filter.currentData(),
            'search_term': self.search_input.text().strip(),
            'date_from': self.date_from.date().toString("yyyy-MM-dd"),
            'date_to': self.date_to.date().toString("yyyy-MM-dd")
        }