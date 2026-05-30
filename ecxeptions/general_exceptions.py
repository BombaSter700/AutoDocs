class AppError(Exception):
    """Базовое исключение для всех ошибок приложения."""

    def __init__(self, message: str = "", detail: str | None = None) -> None:
        self.message = message or "Произошла ошибка приложения"
        self.detail = detail
        super().__init__(self.message)

    def user_message(self) -> str:
        msg = self.message
        if self.detail:
            msg += f"\n\nПодробнее: {self.detail}"
        return msg


class DatabaseError(AppError):
    """Ошибка подключения или выполнения запроса к БД."""

    def __init__(self, message: str = "Ошибка базы данных", detail: str | None = None) -> None:
        super().__init__(message, detail)


class ValidationError(AppError):
    """Ошибка валидации входных данных."""

    def __init__(self, message: str = "Ошибка валидации", detail: str | None = None) -> None:
        super().__init__(message, detail)


class ConfigError(AppError):
    """Ошибка конфигурации приложения (отсутствуют .env, неверные настройки)."""

    def __init__(self, message: str = "Ошибка конфигурации", detail: str | None = None) -> None:
        super().__init__(message, detail)
