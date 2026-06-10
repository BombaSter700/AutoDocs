from PyQt6.QtCore import QSettings, Qt
from qfluentwidgets import FluentWindow, FluentTitleBar
from ui import WindowManager


class BaseMainWindow(FluentWindow):
    def __init__(self, app_name="DesktopSchool", company_name="MySchool"):
        super().__init__()
        self.settings = QSettings(company_name, app_name)
        self.window_manager = None

    def closeEvent(self, event):
        if self.window_manager:
            self.window_manager.save_settings()
        super().closeEvent(event)
