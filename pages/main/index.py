from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget, QListWidgetItem
from PyQt6.QtCore import Qt

from pages.base_window import BaseMainWindow
from pages.dashboard.index import DashboardPage
from pages.equipment.index import EquipmentPage
from pages.document.index import DocumentPage
from pages.movement.index import MovementPage
from pages.maintenance.index import MaintenancePage
from pages.inventory.index import InventoryPage
from pages.write_off.index import WriteOffPage
from pages.network.index import NetworkPage
from pages.employee.index import EmployeePage
from pages.location.index import LocationPage


class MainWindow(BaseMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление оборудованием")
        self.setGeometry(100, 50, 1200, 700)
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(200)
        self.nav_list.currentRowChanged.connect(self._change_page)

        menu_items = [
            "Панель",
            "Оборудование",
            "Документы",
            "Перемещения",
            "Обслуживание",
            "Инвентаризация",
            "Списание",
            "Сеть",
            "Сотрудники",
            "Локации",
        ]
        for item in menu_items:
            self.nav_list.addItem(QListWidgetItem(item))

        self.stacked = QStackedWidget()

        self.pages = {
            0: DashboardPage(),
            1: EquipmentPage(),
            2: DocumentPage(),
            3: MovementPage(),
            4: MaintenancePage(),
            5: InventoryPage(),
            6: WriteOffPage(),
            7: NetworkPage(),
            8: EmployeePage(),
            9: LocationPage(),
        }

        for page in self.pages.values():
            self.stacked.addWidget(page)

        layout.addWidget(self.nav_list)
        layout.addWidget(self.stacked)

    def _change_page(self, index: int) -> None:
        if 0 <= index < self.stacked.count():
            self.stacked.setCurrentIndex(index)

    def apply_scale(self, scale: float) -> None:
        font = self.nav_list.font()
        font.setPointSizeF(10 * scale)
        self.nav_list.setFont(font)

        for page in self.pages.values():
            if hasattr(page, "apply_scale"):
                page.apply_scale(scale)
