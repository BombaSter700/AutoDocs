from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class CardItem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setFixedSize(300, 220)

    def setup_ui(self):
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        
        self.container = QWidget()
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(6)

        
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        self.photo_label = QLabel("Фото")
        self.photo_label.setFixedSize(80, 80)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setStyleSheet("""
            background-color: #EAEAEA;
            border: 1px solid #CCCCCC;
            border-radius: 8px;
        """)

        info_layout = QFormLayout()
        info_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        info_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)

        self.name_label = QLabel("—")
        self.group_label = QLabel("—")
        self.age_label = QLabel("—")
        self.locker = QLabel("—")

        info_layout.addRow("ФИО:", self.name_label)
        info_layout.addRow("Группа:", self.group_label)
        info_layout.addRow("Возраст:", self.age_label)
        info_layout.addRow("Шкафчик:", self.locker)

        top_layout.addWidget(self.photo_label)
        top_layout.addLayout(info_layout)

        
        self.contact_label = QLabel("<b>Контакты:</b>")
        self.phone_label = QLabel("Телефон: —")
        self.email_label = QLabel("Email: —")

        container_layout.addLayout(top_layout)
        container_layout.addWidget(self.contact_label)
        container_layout.addWidget(self.phone_label)
        container_layout.addWidget(self.email_label)
        container_layout.addStretch()

        
        self.container.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #DDD;
                border-radius: 12px;
            }
            QLabel {
                font-size: 13px;
                color: #333333;
            }
        """)

        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.container.setGraphicsEffect(shadow)

        main_layout.addWidget(self.container)

    def load_data(self, student):
        self.name_label.setText(student.get("name", "—"))
        self.group_label.setText(student.get("group", "—"))
        self.age_label.setText(str(student.get("age", "—")))
        self.locker.setText(student.get("locker", "—"))
        self.phone_label.setText(f"Телефон: {student.get('phone', '—')}")
        self.email_label.setText(f"Email: {student.get('email', '—')}")
