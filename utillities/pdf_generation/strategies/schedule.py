from typing import Any, Dict, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

from ..base import BasePdfGenerator


_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

_DAYS_RU: Dict[str, str] = {
    "monday": "Понедельник",
    "tuesday": "Вторник",
    "wednesday": "Среда",
    "thursday": "Четверг",
    "friday": "Пятница",
    "saturday": "Суббота",
}


class SchedulePdfGenerator(BasePdfGenerator):
    def __init__(self, class_name: str, lessons: List[Dict[str, Any]]) -> None:
        self._class_name = class_name
        self._lessons = lessons

    def generate(self, output_path: str) -> str:
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20,
        )

        styles = getSampleStyleSheet()
        styles["Normal"].fontName = "HeiseiMin-W3"
        styles["Title"].fontName = "HeiseiMin-W3"

        elements = [
            Paragraph(f"Расписание класса {self._class_name}", styles["Title"]),
        ]

        table_data = [["Урок", "Время"] + [_DAYS_RU[d] for d in _DAYS]]

        lessons_by_number: Dict[int, List[Dict]] = {}
        for lesson in self._lessons:
            lessons_by_number.setdefault(lesson["lesson_number"], []).append(lesson)

        for lesson_number in sorted(lessons_by_number.keys()):
            row: List[str] = [str(lesson_number), ""]
            lessons_map = {l["day_of_week"]: l for l in lessons_by_number[lesson_number]}

            time = lessons_by_number[lesson_number][0]
            row[1] = f"{time['start_time']} – {time['end_time']}"

            for day in _DAYS:
                lesson = lessons_map.get(day)
                if lesson:
                    text = lesson["subject"]
                    if lesson.get("classroom"):
                        text += f" ({lesson['classroom']})"
                    row.append(text)
                else:
                    row.append("")

            table_data.append(row)

        table = Table(table_data, repeatRows=1)
        table.setStyle(
            TableStyle([
                ("FONT", (0, 0), (-1, -1), "HeiseiMin-W3"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )

        elements.append(table)
        doc.build(elements)

        return output_path
