from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Панель управления")

        layout = QVBoxLayout(self)

        title = QLabel("Панель управления")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        subtitle = QLabel(
            "Система учёта оборудования\n\n"
            "Используйте навигацию слева для работы с разделами."
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #888;")
        layout.addWidget(subtitle)

        layout.addStretch()
