import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator
from qfluentwidgets._rc.resource import qInitResources

from config import init_db
from pages.main.index import MainWindow


if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 9))

    qInitResources()

    translator = FluentTranslator()
    app.installTranslator(translator)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
