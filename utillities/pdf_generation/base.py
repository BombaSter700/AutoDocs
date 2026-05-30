from abc import ABC, abstractmethod


class BasePdfGenerator(ABC):
    @abstractmethod
    def generate(self, output_path: str) -> str:
        ...
