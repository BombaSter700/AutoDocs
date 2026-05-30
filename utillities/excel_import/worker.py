import pandas as pd
from PyQt6.QtCore import QObject, pyqtSignal

from .base import BaseExcelParser, ImportResult


class ExcelImportWorker(QObject):
    started = pyqtSignal()
    progress = pyqtSignal(int)
    finished = pyqtSignal(ImportResult)
    error = pyqtSignal(str)

    def __init__(self, parser: BaseExcelParser, file_path: str) -> None:
        super().__init__()
        self._parser = parser
        self._file_path = file_path

    @property
    def parser(self) -> BaseExcelParser:
        return self._parser

    @property
    def file_path(self) -> str:
        return self._file_path

    def run(self) -> None:
        self.started.emit()
        try:
            self.progress.emit(10)
            df = pd.read_excel(self._file_path, header=None)
            self.progress.emit(50)

            result = self._parser.parse(df)

            self.progress.emit(100)
            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))
