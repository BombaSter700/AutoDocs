from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from qfluentwidgets import BodyLabel, CardWidget


CHART_COLORS = [
    QColor("#0078D4"), QColor("#E67E22"), QColor("#27AE60"),
    QColor("#E74C3C"), QColor("#9B59B6"), QColor("#F39C12"),
    QColor("#1ABC9C"), QColor("#3498DB"), QColor("#2C3E50"),
    QColor("#D35400"),
]


class _DonutCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(160, 160)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data: list[tuple[str, float, QColor]] = []
        self._total = 0.0

    def set_data(self, data, total):
        self._data = data
        self._total = total
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        side = min(self.width(), self.height()) - 20
        if side <= 0:
            painter.end()
            return
        offset_x = (self.width() - side) // 2
        offset_y = (self.height() - side) // 2
        rect = QRectF(offset_x, offset_y, side, side)

        if not self._data:
            painter.setPen(QPen(QColor("#E0E0E0"), 2))
            painter.setBrush(QColor("#F5F5F5"))
            painter.drawEllipse(rect)
            painter.setFont(QFont("Arial", 10))
            painter.setPen(QColor("#999"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Нет данных")
            painter.end()
            return

        painter.setPen(Qt.PenStyle.NoPen)
        start_angle = 90 * 16
        for label, val, color in self._data:
            span = int((val / self._total) * 360 * 16) if self._total > 0 else 0
            painter.setBrush(color)
            painter.drawPie(rect, start_angle, span)
            start_angle += span

        inner_side = side * 0.55
        inner_offset = (side - inner_side) / 2
        inner_rect = QRectF(offset_x + inner_offset, offset_y + inner_offset, inner_side, inner_side)
        painter.setBrush(self._resolve_bg())
        painter.drawEllipse(inner_rect)
        painter.setPen(QColor("#333"))
        font_size = max(10, int(inner_side * 0.18))
        painter.setFont(QFont("Arial", font_size, QFont.Weight.Bold))
        painter.drawText(inner_rect, Qt.AlignmentFlag.AlignCenter, f"{int(self._total)}")
        painter.end()

    def _resolve_bg(self):
        from qfluentwidgets import isDarkTheme
        return QColor("#1E1E1E") if isDarkTheme() else QColor("#FFFFFF")


class _BarCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(140)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data: list[tuple[str, float, QColor]] = []
        self._max_val = 1.0

    def set_data(self, data, max_val):
        self._data = data
        self._max_val = max_val
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        margin = {"left": 8, "right": 8, "top": 20, "bottom": 24}
        if not self._data:
            painter.setFont(QFont("Arial", 10))
            painter.setPen(QColor("#999"))
            painter.drawText(QRectF(0, 0, w, h), Qt.AlignmentFlag.AlignCenter, "Нет данных")
            painter.end()
            return

        count = len(self._data)
        total_spacing = w - margin["left"] - margin["right"]
        gap = max(4, min(12, total_spacing // (count * 4)))
        bar_w = max(12, (total_spacing - gap * (count + 1)) // count)
        start_x = margin["left"] + gap

        for i, (label, val, color) in enumerate(self._data):
            bar_h = int((val / self._max_val) * (h - margin["top"] - margin["bottom"]))
            bar_h = max(1, bar_h)
            x = start_x + i * (bar_w + gap)
            y = h - margin["bottom"] - bar_h

            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x, y, bar_w, bar_h, 3, 3)

            painter.setPen(QColor("#666"))
            painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
            painter.drawText(QRectF(x, y - 16, bar_w, 14), Qt.AlignmentFlag.AlignCenter, str(int(val)))

            painter.setFont(QFont("Arial", 7))
            painter.setPen(QColor("#888"))
            elided = label if len(label) < 10 else label[:9] + "."
            painter.drawText(QRectF(x, h - margin["bottom"] + 2, bar_w, 20), Qt.AlignmentFlag.AlignHCenter, elided)

        painter.end()


class DonutChartWidget(CardWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self._title = title
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        self.title_label = BodyLabel(self._title)
        self.title_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(self.title_label)

        content = QHBoxLayout()
        content.setSpacing(8)
        self._chart = _DonutCanvas(self)
        content.addWidget(self._chart, stretch=3)

        self._legend_layout = QVBoxLayout()
        self._legend_layout.setSpacing(2)
        self._legend_widgets: list[QLabel] = []
        content.addLayout(self._legend_layout, stretch=2)
        layout.addLayout(content)

    def set_data(self, data: list[tuple[str, float]]):
        self._data = data
        total = sum(v for _, v in data)
        self._chart.set_data(
            [(l, v, CHART_COLORS[i % len(CHART_COLORS)]) for i, (l, v) in enumerate(data)],
            total,
        )
        self._update_legend(data, total)

    def _update_legend(self, data, total):
        for w in self._legend_widgets:
            w.deleteLater()
        self._legend_widgets.clear()
        for i, (label, val) in enumerate(data):
            pct = (val / total * 100) if total > 0 else 0
            color = CHART_COLORS[i % len(CHART_COLORS)]
            text = f'{"█"} {label}: {int(val)} ({pct:.1f}%)'
            w = QLabel(text)
            w.setStyleSheet(f"color: {color.name()}; font-size: 11px; padding: 1px 0;")
            self._legend_layout.addWidget(w)
            self._legend_widgets.append(w)


class BarChartWidget(CardWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self._title = title
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        self.title_label = BodyLabel(self._title)
        self.title_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(self.title_label)

        self._canvas = _BarCanvas(self)
        layout.addWidget(self._canvas, stretch=1)

    def set_data(self, data: list[tuple[str, float]]):
        max_val = max(v for _, v in data) if data else 1
        self._canvas.set_data(
            [(l, v, CHART_COLORS[i % len(CHART_COLORS)]) for i, (l, v) in enumerate(data)],
            max_val,
        )
