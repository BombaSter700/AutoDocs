import re
from typing import Dict, List, Optional, Tuple

import pandas as pd

from config.database import engine
from ecxeptions import (
    ExcelHeaderNotFoundError,
    ExcelColumnNotFoundError,
    ExcelEntityNotFoundError,
    ExcelParseError,
    ExcelImportError,
)
from ..base import BaseExcelParser, ImportResult


def _parse_subject_and_classroom(cell_value: str) -> Tuple[Optional[str], Optional[str]]:
    if not cell_value or pd.isna(cell_value):
        return None, None

    pattern = r'^([^(]+)(?:\s*\(([^)]+)\))?$'
    match = re.match(pattern, str(cell_value).strip())

    if match:
        subject_name = match.group(1).strip()
        classroom = match.group(2).strip() if match.group(2) else None
        return subject_name, classroom

    return None, None


def _get_days_mapping() -> Dict[str, str]:
    return {
        'Понедельник': 'monday',
        'Вторник': 'tuesday',
        'Среда': 'wednesday',
        'Четверг': 'thursday',
        'Пятница': 'friday',
        'Суббота': 'saturday',
    }


class ScheduleExcelParser(BaseExcelParser):
    def __init__(self, building_id: int, class_name: str) -> None:
        self._building_id = building_id
        self._class_name = class_name

    def parse(self, df: pd.DataFrame) -> ImportResult:
        schedule_row_idx = None
        for i in range(len(df)):
            value = df.iloc[i, 0]
            if isinstance(value, str) and "РАСПИСАНИЕ" in value.upper():
                schedule_row_idx = i
                break

        if schedule_row_idx is None:
            raise ExcelHeaderNotFoundError("РАСПИСАНИЕ")

        headers_row_idx = schedule_row_idx + 1
        headers = df.iloc[headers_row_idx].tolist()

        days_mapping = _get_days_mapping()
        day_columns: Dict[str, int] = {}

        for idx, header in enumerate(headers):
            if pd.isna(header):
                continue
            header_str = str(header).strip()
            if header_str in days_mapping:
                day_columns[header_str] = idx

        if not day_columns:
            raise ExcelColumnNotFoundError(
                ", ".join(days_mapping.keys())
            )

        raw_conn = engine.raw_connection()
        try:
            cursor = raw_conn.connection.cursor(dictionary=True)

            school_class = self._find_class(cursor)
            if not school_class:
                raise ExcelEntityNotFoundError("Класс", self._class_name)

            lessons_to_create = []

            for row_idx in range(headers_row_idx + 1, len(df)):
                row = df.iloc[row_idx]
                time_cell = row[0]

                if not isinstance(time_cell, str) or "-" not in time_cell:
                    continue

                lesson_number = row_idx - headers_row_idx

                try:
                    start_time, end_time = [t.strip() for t in time_cell.split("-")]
                except ValueError:
                    continue

                for day_name, col_idx in day_columns.items():
                    cell_value = row[col_idx]

                    if pd.isna(cell_value) or not cell_value:
                        continue

                    subject_name, classroom = _parse_subject_and_classroom(cell_value)
                    if not subject_name:
                        raise ExcelParseError(
                            row_idx, col_idx, str(cell_value)
                        )

                    subject = self._get_or_create_subject(cursor, subject_name)

                    lessons_to_create.append({
                        "class_id": school_class["id"],
                        "subject_id": subject["id"],
                        "classroom": classroom,
                        "day_of_week": days_mapping[day_name],
                        "lesson_number": lesson_number,
                        "start_time": start_time,
                        "end_time": end_time,
                    })

            self._save_lessons(cursor, lessons_to_create)
            raw_conn.commit()

        except Exception:
            raw_conn.rollback()
            raise
        finally:
            raw_conn.close()

        return ImportResult(
            success=True,
            data={
                "class_name": self._class_name,
                "lessons_created": len(lessons_to_create),
            },
        )

    def _find_class(self, cursor) -> Optional[Dict]:
        if self._building_id:
            cursor.execute(
                """
                SELECT id, building_id, teacher_id, name
                FROM classes
                WHERE name = %s AND building_id = %s
                """,
                (self._class_name, self._building_id),
            )
        else:
            cursor.execute(
                """
                SELECT id, building_id, teacher_id, name
                FROM classes
                WHERE name = %s
                """,
                (self._class_name,),
            )
        return cursor.fetchone()

    def _get_or_create_subject(self, cursor, subject_name: str) -> Dict:
        cursor.execute(
            "SELECT id, name FROM subjects WHERE name = %s",
            (subject_name,),
        )
        subject = cursor.fetchone()

        if subject:
            return subject

        cursor.execute(
            "INSERT INTO subjects (name) VALUES (%s)",
            (subject_name,),
        )

        return {
            "id": cursor.lastrowid,
            "name": subject_name,
        }

    def _save_lessons(self, cursor, lessons_data: List[Dict]) -> None:
        if not lessons_data:
            return

        class_id = lessons_data[0]["class_id"]

        cursor.execute(
            "DELETE FROM lessons WHERE class_id = %s",
            (class_id,),
        )

        insert_query = """
            INSERT INTO lessons
            (class_id, subject_id, classroom, day_of_week, lesson_number, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        for lesson in lessons_data:
            cursor.execute(
                insert_query,
                (
                    lesson["class_id"],
                    lesson["subject_id"],
                    lesson["classroom"],
                    lesson["day_of_week"],
                    lesson["lesson_number"],
                    lesson["start_time"],
                    lesson["end_time"],
                ),
            )
