import pandas as pd
from PyQt6.QtCore import QObject, pyqtSignal

from ecxeptions import AppError, ExcelImportError, ExcelFileNotFoundError, ExcelInvalidFormatError
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
            import os
            if not os.path.exists(self._file_path):
                raise ExcelFileNotFoundError(self._file_path)

            ext = os.path.splitext(self._file_path)[1].lower()
            if ext not in (".xlsx", ".xls"):
                raise ExcelInvalidFormatError(self._file_path)

            self.progress.emit(10)
            df = pd.read_excel(self._file_path, header=None)
            self.progress.emit(50)

            result = self._parser.parse(df)

            self.progress.emit(100)
            self.finished.emit(result)

        except ExcelImportError as e:
            self.error.emit(e.user_message())
        except AppError as e:
            self.error.emit(e.user_message())
        except Exception as e:
            self.error.emit(f"Неизвестная ошибка: {e}")
