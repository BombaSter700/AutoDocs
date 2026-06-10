from qfluentwidgets import InfoBadge, InfoBadgePosition, InfoLevel


class StatusBadge(InfoBadge):
    STATUS_MAP = {
        "planned": InfoLevel.SUCCESS,
        "in_progress": InfoLevel.WARNING,
        "completed": InfoLevel.INFOAMTION,
        "cancelled": InfoLevel.ERROR,
        "postponed": InfoLevel.WARNING,
    }

    STATUS_TEXT = {
        "planned": "Запланировано",
        "in_progress": "В процессе",
        "completed": "Завершено",
        "cancelled": "Отменено",
        "postponed": "Отложено",
    }

    def __init__(self, status, parent=None):
        level = self.STATUS_MAP.get(status, InfoLevel.INFORMATION)
        text = self.STATUS_TEXT.get(status, status)
        super().__init__(text=text, level=level, parent=parent)
        self._status = status

    def update_status(self, status):
        self._status = status
        level = self.STATUS_MAP.get(status, InfoLevel.INFORMATION)
        text = self.STATUS_TEXT.get(status, status)
        self.level = level
        self.setText(text)

    def get_status(self):
        return self._status
