from datetime import date, datetime
from decimal import Decimal
from typing import Any, Callable, List, Optional, Tuple, Type

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import BodyLabel, PushButton, SearchLineEdit

from config import get_session
from database import Base, BaseRepository


def _get_value(obj: Any, accessor: Any) -> str:
    if callable(accessor):
        val = accessor(obj)
    elif isinstance(accessor, str):
        parts = accessor.split(".")
        val = obj
        for p in parts:
            if val is None:
                break
            val = getattr(val, p, None)
    else:
        val = accessor
    if val is None:
        return "—"
    if isinstance(val, bool):
        return "Да" if val else "Нет"
    if isinstance(val, datetime):
        return val.strftime("%d.%m.%Y %H:%M")
    if isinstance(val, date):
        return val.strftime("%d.%m.%Y")
    if isinstance(val, Decimal):
        return f"{val:,.2f}"
    if isinstance(val, float):
        return f"{val:,.2f}"
    return str(val)


STATUS_COLORS: dict[str, QColor] = {
    "in_use": QColor("#27AE60"),
    "under_maintenance": QColor("#E67E22"),
    "written_off": QColor("#E74C3C"),
    "reserved": QColor("#3498DB"),
    "received": QColor("#2ECC71"),
    "active": QColor("#27AE60"),
    "inactive": QColor("#95A5A6"),
    "faulty": QColor("#E74C3C"),
    "planned": QColor("#3498DB"),
    "in_progress": QColor("#E67E22"),
    "completed": QColor("#27AE60"),
    "cancelled": QColor("#E74C3C"),
    "postponed": QColor("#95A5A6"),
    "pending": QColor("#E67E22"),
    "approved": QColor("#27AE60"),
    "draft": QColor("#95A5A6"),
    "archived": QColor("#95A5A6"),
}


ColumnConfig = Tuple[str, Any, int]


class DataTableWidget(QWidget):
    row_double_clicked = pyqtSignal(object)

    def __init__(
        self,
        model_class: Type[Base],
        columns: List[ColumnConfig],
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._model_class = model_class
        self._columns = columns
        self._rows: List[List[str]] = []
        self._row_ids: List[int] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QHBoxLayout()
        self.search_edit = SearchLineEdit(self)
        self.search_edit.setPlaceholderText("Поиск...")
        self.search_edit.setMaximumWidth(300)
        self.search_edit.textChanged.connect(self._apply_filter)
        toolbar.addWidget(BodyLabel("Поиск:"))
        toolbar.addWidget(self.search_edit)
        toolbar.addStretch()
        self.refresh_btn = PushButton("Обновить")
        self.refresh_btn.clicked.connect(self.load_data)
        toolbar.addWidget(self.refresh_btn)
        layout.addLayout(toolbar)

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels([c[0] for c in columns])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.itemDoubleClicked.connect(self._on_double_click)
        layout.addWidget(self.table)

        self._status_label = BodyLabel("")
        layout.addWidget(self._status_label)

        for i, (_, _, width) in enumerate(columns):
            if width > 0:
                self.table.setColumnWidth(i, width)

    def load_data(self) -> None:
        self._rows = []
        self._row_ids = []
        try:
            with get_session() as session:
                repo = BaseRepository(session, self._model_class)
                records = repo.get_all()
                for r in records:
                    row = [_get_value(r, acc) for _, acc, _ in self._columns]
                    self._rows.append(row)
                    self._row_ids.append(r.id)
        except Exception:
            pass
        self._apply_filter()

    def _apply_filter(self) -> None:
        search = self.search_edit.text().strip().lower()
        if not search:
            self._populate_table(self._rows, self._row_ids)
            return
        filtered_rows: List[List[str]] = []
        filtered_ids: List[int] = []
        for i, row in enumerate(self._rows):
            if any(search in cell.lower() for cell in row):
                filtered_rows.append(row)
                filtered_ids.append(self._row_ids[i])
        self._populate_table(filtered_rows, filtered_ids)

    def _populate_table(self, rows: List[List[str]], ids: List[int]) -> None:
        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                if ids:
                    item.setData(Qt.ItemDataRole.UserRole, ids[row_idx])
                self._apply_status_color(item, text)
                self.table.setItem(row_idx, col_idx, item)

        total = len(self._rows)
        shown = len(rows)
        if shown == total:
            self._status_label.setText(f"Записей: {total}")
        else:
            self._status_label.setText(f"Записей: {shown} (отфильтровано из {total})")

    def _apply_status_color(self, item: QTableWidgetItem, text: str) -> None:
        color = STATUS_COLORS.get(text)
        if color is not None:
            item.setForeground(color)

    def _on_double_click(self, item: QTableWidgetItem) -> None:
        record_id = item.data(Qt.ItemDataRole.UserRole)
        if record_id is not None and self._row_ids:
            idx = self._row_ids.index(record_id)
            self.row_double_clicked.emit(record_id)

    def get_selected_id(self) -> Optional[int]:
        row = self.table.currentRow()
        if row < 0 or not self._row_ids:
            return None
        return self._row_ids[row]

    def refresh(self) -> None:
        self.load_data()
