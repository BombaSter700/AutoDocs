import tempfile
import os
from typing import Optional

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import (
    PushButton, ComboBox, ToolButton, FluentIcon as FIF,
    InfoBar,
)

from ecxeptions import PdfError, PdfGenerationError, PdfLoadError
from utillities.pdf_generation import BasePdfGenerator


class PdfViewer(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.pdf_document = QPdfDocument(self)
        self._current_path: Optional[str] = None

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        controls = QHBoxLayout()

        open_btn = PushButton("Открыть PDF")
        open_btn.setIcon(FIF.OPEN)
        open_btn.clicked.connect(self.open_pdf)

        print_btn = PushButton("Печать")
        print_btn.setIcon(FIF.PRINT)
        print_btn.clicked.connect(self.print_pdf)

        self.zoom_combo = ComboBox()
        self.zoom_combo.addItems([
            "Fit Width", "Fit Page", "50%", "75%",
            "100%", "125%", "150%", "200%",
        ])
        self.zoom_combo.setCurrentText("Fit Width")
        self.zoom_combo.currentTextChanged.connect(self._on_zoom_changed)

        controls.addWidget(open_btn)
        controls.addWidget(print_btn)
        controls.addStretch()
        controls.addWidget(self.zoom_combo)

        layout.addLayout(controls)

        self.pdf_view = QPdfView(self)
        self.pdf_view.setDocument(self.pdf_document)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        layout.addWidget(self.pdf_view)

    def _on_zoom_changed(self, text: str) -> None:
        if text == "Fit Width":
            self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        elif text == "Fit Page":
            self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        else:
            self.pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)
            factor = int(text.replace("%", "")) / 100.0
            self.pdf_view.setZoomFactor(factor)

    def load_pdf(self, file_path: str) -> None:
        self._current_path = file_path
        status = self.pdf_document.load(file_path)
        if status != QPdfDocument.Status.Ready:
            if status == QPdfDocument.Status.Error:
                err = PdfLoadError(file_path)
                InfoBar.warning(self, "Ошибка", err.user_message())

    def open_pdf(self) -> None:
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть PDF", "", "PDF файлы (*.pdf)"
        )
        if file_path:
            self.load_pdf(file_path)

    def generate_and_load(self, generator: BasePdfGenerator) -> None:
        tmp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(tmp_dir, f"pdf_export_{id(generator)}.pdf")

        try:
            generator.generate(pdf_path)
        except PdfError as e:
            InfoBar.critical(self, "PDF", e.user_message())
            return
        except Exception as e:
            err = PdfGenerationError(detail=str(e))
            InfoBar.critical(self, "PDF", err.user_message())
            return

        self.load_pdf(pdf_path)

    def clear(self) -> None:
        self.pdf_document.close()
        self._current_path = None

    def print_pdf(self) -> None:
        if self.pdf_document.pageCount() == 0:
            InfoBar.info(self, "Печать", "PDF не загружен")
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec():
            self._print_document(printer)

    def _print_document(self, printer: QPrinter) -> None:
        from PyQt6.QtGui import QPainter

        painter = QPainter(printer)
        for page in range(self.pdf_document.pageCount()):
            if page > 0:
                printer.newPage()
            image = self.pdf_document.render(
                page, printer.pageRect().size()
            )
            painter.drawImage(0, 0, image)
        painter.end()
