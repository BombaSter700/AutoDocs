from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget

from database import WriteOffAct, WriteOffActCreate, WriteOffActRead


class WriteOffPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Списание")

        layout = QVBoxLayout(self)

        title = QLabel("Списание имущества")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(self._create_list_tab(), "Акты")
        tabs.addTab(self._create_add_tab(), "Новый акт")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Акты списания (в разработке)"))
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Форма акта списания (в разработке)"))
        return w
