from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class ImportResult:
    success: bool = True
    message: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


class BaseExcelParser(ABC):
    @abstractmethod
    def parse(self, df: pd.DataFrame) -> ImportResult:
        ...
