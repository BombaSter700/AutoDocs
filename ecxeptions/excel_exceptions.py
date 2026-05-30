from .general_exceptions import AppError


class ExcelImportError(AppError):
    """Базовое исключение для ошибок импорта Excel."""

    def __init__(self, message: str = "Ошибка импорта Excel", detail: str | None = None) -> None:
        super().__init__(message, detail)


class ExcelFileNotFoundError(ExcelImportError):
    """Файл Excel не найден по указанному пути."""

    def __init__(self, path: str) -> None:
        super().__init__(
            message="Файл Excel не найден",
            detail=f"Путь: {path}",
        )


class ExcelInvalidFormatError(ExcelImportError):
    """Файл имеет неверный формат (не xlsx/xls)."""

    def __init__(self, path: str) -> None:
        super().__init__(
            message="Неверный формат файла",
            detail=f"Ожидается .xlsx или .xls, получен: {path}",
        )


class ExcelHeaderNotFoundError(ExcelImportError):
    """В файле не найден заголовок (например, 'РАСПИСАНИЕ')."""

    def __init__(self, expected_header: str = "") -> None:
        msg = f"Заголовок '{expected_header}' не найден" if expected_header else "Заголовок не найден"
        super().__init__(
            message="Неверная структура Excel",
            detail=msg,
        )


class ExcelColumnNotFoundError(ExcelImportError):
    """Не найдены ожидаемые колонки (дни недели, поля)."""

    def __init__(self, columns: str = "") -> None:
        super().__init__(
            message="Колонки не найдены",
            detail=f"Ожидаемые колонки: {columns}",
        )


class ExcelEntityNotFoundError(ExcelImportError):
    """Сущность (класс, сотрудник и т.д.) не найдена в БД."""

    def __init__(self, entity_type: str, value: str) -> None:
        super().__init__(
            message=f"{entity_type} не найден(а)",
            detail=f"'{value}' отсутствует в базе данных",
        )


class ExcelParseError(ExcelImportError):
    """Ошибка парсинга ячейки/строки."""

    def __init__(self, row: int, col: int, raw_value: str = "") -> None:
        detail = f"Строка {row}, колонка {col}"
        if raw_value:
            detail += f", значение: '{raw_value}'"
        super().__init__(
            message="Ошибка парсинга данных",
            detail=detail,
        )
