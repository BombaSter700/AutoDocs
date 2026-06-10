from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, CardWidget, StrongBodyLabel, TitleLabel

from config import get_session
from database import (
    Document,
    Employee,
    Equipment,
    EquipmentMovement,
    InventoryCheck,
    Location,
    MaintenanceRecord,
    NetworkNode,
    WriteOffAct,
)
from database.repository import BaseRepository
from ui.components.chart_widgets import BarChartWidget, DonutChartWidget
from utillities.animations import animate_counter


class _StatCard(CardWidget):
    def __init__(self, title: str, value: str, subtitle: str = "", icon: str = "", color: str = "#0078D4", parent=None):
        super().__init__(parent)
        self._target = int(value) if value.isdigit() else 0
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(4)

        header = QHBoxLayout()
        if icon:
            il = BodyLabel(icon)
            il.setStyleSheet("font-size: 26px;")
            header.addWidget(il)
        tl = StrongBodyLabel(title)
        tl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(tl)
        header.addStretch()
        layout.addLayout(header)

        self.value_label = TitleLabel("0")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setStyleSheet(f"font-size: 36px; color: {color}; font-weight: bold;")
        layout.addWidget(self.value_label)

        sl = BodyLabel(subtitle)
        sl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sl.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(sl)

    def animate_value(self):
        anim = animate_counter(self.value_label, self._target, 800)
        self._anim_ref = anim


class _AlertCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.title = StrongBodyLabel("Требуют внимания")
        self.title.setStyleSheet("color: #E67E22; font-size: 13px;")
        layout.addWidget(self.title)
        self._box = QVBoxLayout()
        layout.addLayout(self._box)
        layout.addStretch()

    def set_alerts(self, alerts: list[tuple[str, str, str]]):
        for i in reversed(range(self._box.count())):
            w = self._box.itemAt(i).widget()
            if w:
                w.deleteLater()
        if not alerts:
            lbl = BodyLabel("Всё в порядке")
            lbl.setStyleSheet("color: #27AE60; font-size: 11px;")
            self._box.addWidget(lbl)
            return
        for icon, text, color in alerts:
            lbl = BodyLabel(f"{icon} {text}")
            lbl.setStyleSheet(f"color: {color}; font-size: 11px; padding: 2px 0;")
            self._box.addWidget(lbl)


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Панель управления")
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        self.title = TitleLabel("Панель управления")
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(self.title)

        data = self._collect_all()

        self._build_stats(layout, data)
        self._build_charts(layout, data)
        self._build_info(layout, data)

        layout.addStretch()

        QTimer.singleShot(300, self._animate_all)

    def _build_stats(self, layout, d):
        grid = QGridLayout()
        grid.setSpacing(8)

        cards = [
            ("🖥", "Оборудование", d["equipment"], "всего единиц", "#0078D4"),
            ("👤", "Сотрудники", d["employees"], "человек", "#27AE60"),
            ("📍", "Локации", d["locations"], "помещений", "#9B59B6"),
            ("✅", "В эксплуатации", d["active_eq"], "активно", "#2ECC71"),
            ("🔧", "Обслуживание", d["maintenance"], "записей", "#E67E22"),
            ("📄", "Документы", d["documents"], "всего", "#1ABC9C"),
            ("🌐", "Узлы сети", d["network_nodes"], "узлов", "#E74C3C"),
            ("📦", "Перемещения", d["movements"], "всего", "#F39C12"),
            ("📋", "Инвентаризации", d["inventory_checks"], "проверок", "#3498DB"),
        ]

        self._stat_cards = []
        for i, (icon, title, value, subtitle, color) in enumerate(cards):
            card = _StatCard(title, str(value), subtitle, icon, color)
            grid.addWidget(card, i // 3, i % 3)
            self._stat_cards.append(card)

        layout.addLayout(grid)

    def _build_charts(self, layout, d):
        row = QHBoxLayout()
        row.setSpacing(8)

        dc = DonutChartWidget("По статусам")
        dc.set_data(d["status_dist"])
        row.addWidget(dc)

        bc = BarChartWidget("По категориям")
        bc.set_data(d["cat_dist"])
        row.addWidget(bc)

        layout.addLayout(row)

    def _build_info(self, layout, d):
        row = QHBoxLayout()
        row.setSpacing(8)

        # activity
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setSpacing(2)
        vl.addWidget(StrongBodyLabel("Последние перемещения"))
        for item in d["recent_movements"][:6]:
            vl.addWidget(BodyLabel(f"• {item}"))
        if not d["recent_movements"]:
            vl.addWidget(BodyLabel("Нет записей"))
        vl.addStretch()
        row.addWidget(w)

        # alerts
        ac = _AlertCard()
        ac.set_alerts(self._collect_alerts(d))
        row.addWidget(ac)

        layout.addLayout(row)

    def _animate_all(self):
        for card in self._stat_cards:
            card.animate_value()

    def _collect_all(self) -> dict:
        d = {
            "equipment": 0, "employees": 0, "locations": 0,
            "documents": 0, "maintenance": 0, "inventory_checks": 0,
            "network_nodes": 0, "movements": 0, "write_offs": 0,
            "active_eq": 0, "under_maintenance_count": 0,
            "status_dist": [], "cat_dist": [],
            "recent_movements": [],
        }
        try:
            with get_session() as session:
                eqs = BaseRepository(session, Equipment).get_all()
                d["equipment"] = len(eqs)
                d["employees"] = len(BaseRepository(session, Employee).get_all())
                d["locations"] = len(BaseRepository(session, Location).get_all())
                d["documents"] = len(BaseRepository(session, Document).get_all())
                d["maintenance"] = len(BaseRepository(session, MaintenanceRecord).get_all())
                d["inventory_checks"] = len(BaseRepository(session, InventoryCheck).get_all())
                d["network_nodes"] = len(BaseRepository(session, NetworkNode).get_all())
                d["movements"] = len(BaseRepository(session, EquipmentMovement).get_all())
                d["write_offs"] = len(BaseRepository(session, WriteOffAct).get_all())

                d["active_eq"] = sum(1 for e in eqs if e.status == "in_use")
                d["under_maintenance_count"] = sum(1 for e in eqs if e.status == "under_maintenance")

                sm: dict[str, int] = {}
                for e in eqs:
                    s = e.status or "unknown"
                    sm[s] = sm.get(s, 0) + 1
                labels = {
                    "in_use": "В эксплуатации", "under_maintenance": "На ТО",
                    "written_off": "Списано", "reserved": "В резерве",
                    "received": "Поступило",
                }
                d["status_dist"] = [(labels.get(k, k), float(v)) for k, v in sm.items()]

                cm: dict[str, int] = {}
                for e in eqs:
                    c = e.category or "Прочее"
                    cm[c] = cm.get(c, 0) + 1
                d["cat_dist"] = [(k, float(v)) for k, v in sorted(cm.items(), key=lambda x: -x[1])[:8]]

                items = []
                for m in BaseRepository(session, EquipmentMovement).get_all()[-8:]:
                    eq_name = m.equipment.name[:24] if m.equipment else "?"
                    ds = m.moved_at.strftime("%d.%m") if m.moved_at else "??"
                    fl = m.from_location.name[:12] if m.from_location else "склад"
                    tl = m.to_location.name[:12] if m.to_location else "склад"
                    items.append(f"[{ds}] {eq_name}: {fl}->{tl}")
                d["recent_movements"] = items[::-1]

        except Exception:
            pass
        return d

    @staticmethod
    def _collect_alerts(d) -> list[tuple[str, str, str]]:
        alerts = []
        if d.get("under_maintenance_count", 0) > 0:
            alerts.append(("🔧", f'{d["under_maintenance_count"]} ед. на обслуживании', "#E67E22"))
        if d.get("write_offs", 0) > 0:
            pass
        return alerts
