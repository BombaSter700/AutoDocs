from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QWidget
from qfluentwidgets import CardWidget, TitleLabel, BodyLabel, StrongBodyLabel

from config import get_session
from database import (
    Employee,
    Equipment,
    InventoryCheck,
    Location,
    MaintenanceRecord,
    NetworkNode,
)
from database.repository import BaseRepository


class _StatCard(CardWidget):
    def __init__(self, title: str, value: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = StrongBodyLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label = TitleLabel(value)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setStyleSheet("font-size: 36px;")
        self.subtitle_label = BodyLabel(subtitle)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Панель управления")

        layout = QVBoxLayout(self)
        title = TitleLabel("Панель управления")
        layout.addWidget(title)

        stats = self._collect_stats()

        grid = QGridLayout()
        grid.setSpacing(16)
        cards = [
            _StatCard("Оборудование", str(stats["equipment"]), "всего единиц"),
            _StatCard("Сотрудники", str(stats["employees"]), "человек"),
            _StatCard("Локации", str(stats["locations"]), "помещений"),
            _StatCard("Активное оборудование", str(stats["active_equipment"]), "в эксплуатации"),
            _StatCard("Обслуживание", str(stats["maintenance"]), "записей"),
            _StatCard("Инвентаризации", str(stats["inventory_checks"]), "проверок"),
        ]
        for i, card in enumerate(cards):
            grid.addWidget(card, i // 3, i % 3)

        layout.addLayout(grid)
        subtitle = BodyLabel(
            "Система учёта оборудования\nИспользуйте навигацию слева для работы с разделами."
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        layout.addStretch()

    def _collect_stats(self) -> dict:
        stats = {}
        try:
            with get_session() as session:
                stats["equipment"] = len(BaseRepository(session, Equipment).get_all())
                stats["employees"] = len(BaseRepository(session, Employee).get_all())
                stats["locations"] = len(BaseRepository(session, Location).get_all())
                stats["maintenance"] = len(BaseRepository(session, MaintenanceRecord).get_all())
                stats["inventory_checks"] = len(BaseRepository(session, InventoryCheck).get_all())
                all_eq = BaseRepository(session, Equipment).get_all()
                stats["active_equipment"] = sum(1 for e in all_eq if e.status == "in_use")
        except Exception:
            stats = {
                "equipment": 0, "employees": 0, "locations": 0,
                "active_equipment": 0, "maintenance": 0, "inventory_checks": 0,
            }
        return stats
