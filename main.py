import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from qfluentwidgets import (
    FluentTranslator, setTheme, Theme,
    qconfig, QConfig,
)
from qfluentwidgets._rc.resource import qInitResources

from config import init_db
from pages.main.index import MainWindow


if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    qInitResources()
    setTheme(Theme.AUTO)

    translator = FluentTranslator()
    app.installTranslator(translator)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
