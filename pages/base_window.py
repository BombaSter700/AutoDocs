from PyQt6.QtWidgets import QMainWindow, QDockWidget
from PyQt6.QtCore import QSettings, Qt
from ui import WindowManager

class BaseMainWindow(QMainWindow):
    """Базовый класс для всех окон с поддержкой настроек"""
    
    def __init__(self, app_name="DesktopSchool", company_name="MySchool"):
        super().__init__()
        self.settings = QSettings(company_name, app_name)
        self.window_manager = None
        
    def apply_scale(self, scale):
        """Применение масштаба ко всему окну"""
        # Этот метод можно переопределить в дочерних классах
        # для применения масштаба к специфическому содержимому
        print(f"Применен масштаб: {scale}")
        
    def closeEvent(self, event):
        """Сохранение настроек при закрытии"""
        if self.window_manager:
            self.window_manager.save_settings()
        super().closeEvent(event)