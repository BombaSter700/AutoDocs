from pathlib import Path
from typing import Any, Dict, Optional

from docxtpl import DocxTemplate

from ..base import BasePdfGenerator


class DocxTemplateGenerator(BasePdfGenerator):
    def __init__(
        self,
        template_path: str,
        context: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> None:
        self._template = Path(template_path)
        self._context = context
        self._output_dir = Path(output_dir) if output_dir else Path.cwd()

    def generate(self, output_path: str) -> str:
        path = self._output_dir / output_path
        path.parent.mkdir(parents=True, exist_ok=True)

        doc = DocxTemplate(str(self._template))
        doc.render(self._context)
        doc.save(str(path))

        return str(path)
