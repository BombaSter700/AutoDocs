from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation, pyqtProperty, QTimer
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect


class CounterHelper(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0.0

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value

    counter_value = pyqtProperty(float, _get_value, _set_value)


def animate_counter(label, end_value: int, duration: int = 800):
    helper = CounterHelper(label)
    anim = QPropertyAnimation(helper, b"counter_value")
    anim.setStartValue(0)
    anim.setEndValue(float(end_value))
    anim.setDuration(duration)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def on_value(val):
        label.setText(str(int(val)))

    anim.valueChanged.connect(on_value)
    anim.start()
    return anim


class FadeInAnimation(QPropertyAnimation):
    def __init__(self, widget, duration=300):
        self.effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(self.effect)
        super().__init__(self.effect, b"opacity")
        self.setDuration(duration)
        self.setStartValue(0.0)
        self.setEndValue(1.0)
        self.setEasingCurve(QEasingCurve.Type.OutCubic)


class AnimatedProgressBar(QWidget):
    def __init__(self, parent=None, color="#0078D4"):
        super().__init__(parent)
        self._progress = 0.0
        self._color = color
        self.setFixedHeight(8)
        self.setMinimumWidth(100)

    def set_progress(self, value: float, animated=True):
        if animated:
            self.anim = QPropertyAnimation(self, b"progress")
            self.anim.setStartValue(self._progress)
            self.anim.setEndValue(value)
            self.anim.setDuration(500)
            self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.anim.start()
        else:
            self._progress = value
            self.update()

    def _get_progress(self):
        return self._progress

    def _set_progress(self, value):
        self._progress = value
        self.update()

    progress = pyqtProperty(float, _get_progress, _set_progress)

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QColor, QLinearGradient
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#E0E0E0"))
        painter.drawRoundedRect(0, 0, w, h, h // 2, h // 2)
        fill_w = int(w * min(self._progress / 100.0, 1.0))
        if fill_w > 0:
            gradient = QLinearGradient(0, 0, fill_w, 0)
            base = QColor(self._color)
            gradient.setColorAt(0, base.lighter(120))
            gradient.setColorAt(1, base)
            painter.setBrush(gradient)
            painter.drawRoundedRect(0, 0, fill_w, h, h // 2, h // 2)
        painter.end()
