from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class StatusBadge(QWidget):
    """Компонент для отображения статуса с цветовым кодированием"""
    
    STATUS_CONFIG = {
        'planned': {'text': 'Запланировано', 'color': '#2e7d32', 'bg_color': '#e8f5e8'},
        'in_progress': {'text': 'В процессе', 'color': '#f9a825', 'bg_color': '#fff8e1'},
        'completed': {'text': 'Завершено', 'color': '#1565c0', 'bg_color': '#e3f2fd'},
        'cancelled': {'text': 'Отменено', 'color': '#c62828', 'bg_color': '#ffebee'},
        'postponed': {'text': 'Отложено', 'color': '#ef6c00', 'bg_color': '#fff3e0'}
    }
    
    def __init__(self, status, parent=None):
        super().__init__(parent)
        self.status = status
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 9, QFont.Weight.Medium))
        
        self.update_status(self.status)
        layout.addWidget(self.label)
        
    def update_status(self, status):
        """Обновление отображаемого статуса"""
        self.status = status
        config = self.STATUS_CONFIG.get(status, {'text': status, 'color': '#666', 'bg_color': '#f5f5f5'})
        
        self.label.setText(config['text'])
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {config['color']};
                background-color: {config['bg_color']};
                border: 1px solid {config['color']}20;
                border-radius: 8px;
                padding: 4px 8px;
                font-weight: bold;
            }}
        """)
    
    def get_status(self):
        return self.status