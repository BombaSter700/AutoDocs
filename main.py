import sys
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from pages.main.index import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())