from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QLabel
from qfluentwidgets import CardWidget, BodyLabel


class CardItem(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 220)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

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
        info_layout.setSpacing(4)

        self.name_label = BodyLabel("—")
        self.group_label = BodyLabel("—")
        self.age_label = BodyLabel("—")
        self.locker = BodyLabel("—")

        info_layout.addRow("ФИО:", self.name_label)
        info_layout.addRow("Группа:", self.group_label)
        info_layout.addRow("Возраст:", self.age_label)
        info_layout.addRow("Шкафчик:", self.locker)

        top_layout.addWidget(self.photo_label)
        top_layout.addLayout(info_layout)

        self.contact_label = BodyLabel("<b>Контакты:</b>")
        self.phone_label = BodyLabel("Телефон: —")
        self.email_label = BodyLabel("Email: —")

        layout.addLayout(top_layout)
        layout.addWidget(self.contact_label)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.email_label)
        layout.addStretch()

    def load_data(self, student):
        self.name_label.setText(student.get("name", "—"))
        self.group_label.setText(student.get("group", "—"))
        self.age_label.setText(str(student.get("age", "—")))
        self.locker.setText(student.get("locker", "—"))
        self.phone_label.setText(f"Телефон: {student.get('phone', '—')}")
        self.email_label.setText(f"Email: {student.get('email', '—')}")
