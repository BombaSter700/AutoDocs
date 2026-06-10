from PyQt6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF, NavigationItemPosition

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
from ui import WindowManager
from PyQt6.QtWidgets import QWidget


class MainWindow(BaseMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление оборудованием")

        self._init_navigation()

        self.window_manager = WindowManager(self)
        self.window_manager.setup_window_shortcuts(self)

    def _init_navigation(self):
        pages = [
            (DashboardPage(), FIF.HOME, "Панель"),
            (EquipmentPage(), FIF.DEVELOPER_TOOLS, "Оборудование"),
            (DocumentPage(), FIF.DOCUMENT, "Документы"),
            (MovementPage(), FIF.MOVE, "Перемещения"),
            (MaintenancePage(), FIF.SPEED_HIGH, "Обслуживание"),
            (InventoryPage(), FIF.CHECKBOX, "Инвентаризация"),
            (WriteOffPage(), FIF.DELETE, "Списание"),
            (NetworkPage(), FIF.CONNECT, "Сеть"),
            (EmployeePage(), FIF.PEOPLE, "Сотрудники"),
            (LocationPage(), FIF.FOLDER, "Локации"),
        ]

        for page, icon, text in pages:
            page.setObjectName(text.lower().replace(" ", "_"))
            self.addSubInterface(page, icon, text, NavigationItemPosition.TOP)

    def apply_scale(self, scale: float) -> None:
        for i in range(self.stackedWidget.count()):
            w = self.stackedWidget.widget(i)
            if hasattr(w, "apply_scale"):
                w.apply_scale(scale)
