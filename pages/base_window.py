from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QAction, QKeySequence
from qfluentwidgets import FluentWindow
from ui import WindowManager
from ui.styles import apply_theme


class BaseMainWindow(FluentWindow):
    def __init__(self, app_name="DesktopSchool", company_name="MySchool"):
        super().__init__()
        self.settings = QSettings(company_name, app_name)
        self.window_manager = None
        self._load_theme()

    def _load_theme(self):
        theme = self.settings.value("theme_mode", "auto")
        apply_theme(theme)

    def _save_theme(self, mode: str):
        self.settings.setValue("theme_mode", mode)

    def closeEvent(self, event):
        if self.window_manager:
            self.window_manager.save_settings()
        super().closeEvent(event)

    def apply_scale(self, scale: float) -> None:
        for i in range(self.stackedWidget.count()):
            w = self.stackedWidget.widget(i)
            if hasattr(w, "apply_scale"):
                w.apply_scale(scale)
