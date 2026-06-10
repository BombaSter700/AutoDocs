from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import TabWidget, TitleLabel, BodyLabel

from database import NetworkNode, NetworkLink
from utillities.useTables import DataTableWidget


class NetworkPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Сетевая инфраструктура")

        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("Сетевая инфраструктура"))

        tabs = TabWidget(self)
        tabs.addTab(self._create_nodes_tab(), "Узлы")
        tabs.addTab(self._create_links_tab(), "Соединения")
        layout.addWidget(tabs)

    def _create_nodes_tab(self) -> QWidget:
        columns = [
            ("Имя", "name", 200),
            ("Тип", "node_type", 120),
            ("IP-адрес", "ip_address", 130),
            ("MAC-адрес", "mac_address", 140),
            ("Производитель", "vendor", 140),
            ("Модель", "model", 140),
            ("Статус", "status", 80),
            ("Локация", "location.name", 180),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table_nodes = DataTableWidget(NetworkNode, columns)
        layout.addWidget(self.table_nodes)
        return w

    def _create_links_tab(self) -> QWidget:
        columns = [
            ("От узла", "from_node.name", 180),
            ("Порт (от)", "port_from", 80),
            ("К узлу", "to_node.name", 180),
            ("Порт (к)", "port_to", 80),
            ("Тип", "link_type", 100),
            ("Статус", "status", 80),
            ("Примечания", "notes", 200),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table_links = DataTableWidget(NetworkLink, columns)
        layout.addWidget(self.table_links)
        return w
