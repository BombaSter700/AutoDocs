from .general_exceptions import AppError


class PdfError(AppError):
    """Базовое исключение для ошибок PDF."""

    def __init__(self, message: str = "Ошибка работы с PDF", detail: str | None = None) -> None:
        super().__init__(message, detail)


class PdfGenerationError(PdfError):
    """Ошибка генерации PDF (ReportLab)."""

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            message="Ошибка генерации PDF",
            detail=detail,
        )


class PdfLoadError(PdfError):
    """Не удалось загрузить PDF-документ."""

    def __init__(self, path: str = "") -> None:
        super().__init__(
            message="Не удалось загрузить PDF",
            detail=f"Путь: {path}" if path else None,
        )


class PdfPrintError(PdfError):
    """Ошибка печати PDF."""

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            message="Ошибка печати PDF",
            detail=detail,
        )


class PdfRenderError(PdfError):
    """Ошибка рендеринга страницы PDF."""

    def __init__(self, page: int = 0, detail: str | None = None) -> None:
        msg = f"Ошибка рендеринга страницы {page}" if page else "Ошибка рендеринга PDF"
        super().__init__(message=msg, detail=detail)
