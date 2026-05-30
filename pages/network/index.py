from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget

from database import NetworkNode, NetworkLink, NetworkNodeCreate, NetworkLinkCreate


class NetworkPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Сетевая инфраструктура")

        layout = QVBoxLayout(self)

        title = QLabel("Сетевая инфраструктура")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(self._create_nodes_tab(), "Узлы")
        tabs.addTab(self._create_links_tab(), "Соединения")
        layout.addWidget(tabs)

    def _create_nodes_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Таблица узлов сети (в разработке)"))
        return w

    def _create_links_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("Схема соединений (в разработке)"))
        return w
