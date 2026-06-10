from qfluentwidgets import setTheme, setThemeColor, Theme, qconfig, QConfig
from PyQt6.QtGui import QColor

ACCENT_COLOR = QColor("#0078D4")
SUCCESS_COLOR = "#27AE60"
WARNING_COLOR = "#E67E22"
DANGER_COLOR = "#E74C3C"
INFO_COLOR = "#3498DB"

DASHBOARD_CARD_STYLE = """
CardWidget {{
    border-radius: 8px;
    border: 1px solid {border};
    background-color: {bg};
}}
"""

TABLE_ALTERNATE_COLORS = ["#F8F9FA", "#FFFFFF"]


def apply_theme(mode: str):
    if mode == "light":
        setTheme(Theme.LIGHT)
    elif mode == "dark":
        setTheme(Theme.DARK)
    else:
        setTheme(Theme.AUTO)
    setThemeColor(ACCENT_COLOR)


def get_accent_color():
    return ACCENT_COLOR
