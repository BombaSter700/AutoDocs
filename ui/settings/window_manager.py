from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSettings, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import (
    PushButton, ComboBox, SwitchButton, BodyLabel,
    FluentIcon as FIF, PrimaryPushButton,
)


class WindowManager(QWidget):
    scale_changed = pyqtSignal(float)
    fullscreen_changed = pyqtSignal(bool)

    def __init__(self, parent=None, app_name="MyApp", company_name="MyCompany"):
        super().__init__(parent)
        self.parent_window = parent
        self.settings = QSettings(company_name, app_name)
        self.current_scale = 1.0
        self._setup_ui()
        self.load_settings()

    def _setup_ui(self):
        self.setFixedWidth(280)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        title = BodyLabel("Настройки окна")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 8px 0;")
        layout.addWidget(title)

        # --- Масштаб ---
        layout.addWidget(BodyLabel("Масштаб:"))

        self.scale_combo = ComboBox()
        self.scale_combo.addItems(["75%", "100%", "125%", "150%", "175%", "200%"])
        self.scale_combo.currentTextChanged.connect(self._change_scale_combo)
        layout.addWidget(self.scale_combo)

        zoom_layout = QHBoxLayout()
        self.zoom_out_btn = PushButton("Уменьшить")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.zoom_in_btn = PushButton("Увеличить")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(self.zoom_out_btn)
        zoom_layout.addWidget(self.zoom_in_btn)
        layout.addLayout(zoom_layout)

        # --- Окно ---
        layout.addSpacing(8)

        self.fullscreen_btn = PrimaryPushButton("Полный экран (F11)")
        self.fullscreen_btn.setIcon(FIF.FULL_SCREEN)
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        layout.addWidget(self.fullscreen_btn)

        self.normal_btn = PushButton("Оконный режим")
        self.normal_btn.clicked.connect(self.normal_screen)
        layout.addWidget(self.normal_btn)

        always_on_top_layout = QHBoxLayout()
        always_on_top_layout.addWidget(BodyLabel("Поверх всех окон"))
        always_on_top_layout.addStretch()
        self.always_on_top = SwitchButton()
        self.always_on_top.checkedChanged.connect(self.toggle_always_on_top)
        always_on_top_layout.addWidget(self.always_on_top)
        layout.addLayout(always_on_top_layout)

        layout.addSpacing(8)

        reset_btn = PushButton("Сбросить настройки")
        reset_btn.clicked.connect(self.reset_settings)
        layout.addWidget(reset_btn)

        layout.addStretch()

    def load_settings(self):
        scale = self.settings.value("window_scale", 1.0, type=float)
        self.current_scale = scale
        self._update_scale_combo()

        always_on_top = self.settings.value("always_on_top", False, type=bool)
        self.always_on_top.setChecked(always_on_top)

    def save_settings(self):
        self.settings.setValue("window_scale", self.current_scale)
        self.settings.setValue("always_on_top", self.always_on_top.isChecked())

    def _update_scale_combo(self):
        scale_text = f"{int(self.current_scale * 100)}%"
        index = self.scale_combo.findText(scale_text)
        if index >= 0:
            self.scale_combo.setCurrentIndex(index)

    def _change_scale_combo(self, scale_text):
        scale_map = {
            "75%": 0.75,
            "100%": 1.0,
            "125%": 1.25,
            "150%": 1.5,
            "175%": 1.75,
            "200%": 2.0,
        }
        new_scale = scale_map.get(scale_text, 1.0)
        self.set_scale(new_scale)

    def set_scale(self, scale):
        self.current_scale = max(0.5, min(3.0, scale))
        self.scale_changed.emit(self.current_scale)
        self._update_scale_combo()
        self.save_settings()

    def zoom_in(self):
        self.set_scale(round(self.current_scale + 0.1, 1))

    def zoom_out(self):
        self.set_scale(round(self.current_scale - 0.1, 1))

    def toggle_fullscreen(self):
        if self.parent_window:
            if self.parent_window.isFullScreen():
                self.parent_window.showNormal()
            else:
                self.parent_window.showFullScreen()
            self.fullscreen_changed.emit(self.parent_window.isFullScreen())

    def normal_screen(self):
        if self.parent_window:
            self.parent_window.showNormal()
            self.fullscreen_changed.emit(False)

    def toggle_always_on_top(self, checked):
        if self.parent_window:
            flags = self.parent_window.windowFlags()
            if checked:
                flags |= Qt.WindowType.WindowStaysOnTopHint
            else:
                flags &= ~Qt.WindowType.WindowStaysOnTopHint
            self.parent_window.setWindowFlags(flags)
            self.parent_window.show()
            self.save_settings()

    def reset_settings(self):
        self.set_scale(1.0)
        self.always_on_top.setChecked(False)
        if self.parent_window:
            self.parent_window.showNormal()

    def setup_window_shortcuts(self, window):
        fullscreen_action = QAction(window)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        window.addAction(fullscreen_action)

        escape_action = QAction(window)
        escape_action.setShortcut(QKeySequence("Escape"))
        escape_action.triggered.connect(self.escape_pressed)
        window.addAction(escape_action)

        zoom_in_action = QAction(window)
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        zoom_in_action.triggered.connect(self.zoom_in)
        window.addAction(zoom_in_action)

        zoom_out_action = QAction(window)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self.zoom_out)
        window.addAction(zoom_out_action)

    def escape_pressed(self):
        if self.parent_window and self.parent_window.isFullScreen():
            self.normal_screen()
