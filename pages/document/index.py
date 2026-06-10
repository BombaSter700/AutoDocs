from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import (
    TabWidget, BodyLabel, TitleLabel, PrimaryPushButton,
    ComboBox, LineEdit, PlainTextEdit, InfoBar, InfoBarPosition,
    GroupHeaderCardWidget, CardWidget, StrongBodyLabel,
)

from database import Document
from utillities.useTables import DataTableWidget
from utillities.pdf_generation import DocxTemplateGenerator


def _get_template_list() -> list[Path]:
    docs_dir = Path(__file__).parent.parent.parent / "docs"
    return sorted(docs_dir.glob("*.docx"))


class _GenerateTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        template_card = GroupHeaderCardWidget(self)
        template_card.setTitle("Шаблон")
        self.template_combo = ComboBox()
        templates = _get_template_list()
        if templates:
            for t in templates:
                self.template_combo.addItem(t.stem, str(t))
        else:
            self.template_combo.addItem("Нет шаблонов", "")
        template_card.addGroup(FIF.DOCUMENT, "Выберите шаблон", "", self.template_combo)
        layout.addWidget(template_card)

        text_card = GroupHeaderCardWidget(self)
        text_card.setTitle("Содержимое документа")
        self.text_edit = PlainTextEdit(self)
        self.text_edit.setPlaceholderText("Введите текст, который будет перенесён в документ...")
        self.text_edit.setMinimumHeight(200)
        text_card.addGroup(FIF.EDIT, "Текст документа", "", self.text_edit)
        layout.addWidget(text_card)

        file_card = GroupHeaderCardWidget(self)
        file_card.setTitle("Сохранить как")
        self.file_name_edit = LineEdit(self)
        self.file_name_edit.setPlaceholderText("мой_документ.docx")
        file_card.addGroup(FIF.SAVE_AS, "Имя файла", "", self.file_name_edit)
        self.output_dir_edit = LineEdit(self)
        self.output_dir_edit.setPlaceholderText("Оставить пустым — сохранить рядом с проектом")
        file_card.addGroup(FIF.FOLDER_ADD, "Папка (необяз.)", "", self.output_dir_edit)
        layout.addWidget(file_card)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.generate_btn = PrimaryPushButton("Сгенерировать документ")
        self.generate_btn.setMinimumHeight(44)
        self.generate_btn.clicked.connect(self._on_generate)
        btn_layout.addWidget(self.generate_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        layout.addStretch()

    def _on_generate(self):
        template_path = self.template_combo.currentData()
        if not template_path or not Path(template_path).exists():
            InfoBar.warning(self, "Ошибка", "Выберите существующий шаблон")
            return

        text = self.text_edit.toPlainText().strip()
        if not text:
            InfoBar.warning(self, "Ошибка", "Введите текст документа")
            return

        file_name = self.file_name_edit.text().strip()
        if not file_name:
            file_name = "сгенерированный_документ.docx"
        if not file_name.endswith(".docx"):
            file_name += ".docx"

        output_dir = self.output_dir_edit.text().strip() or None

        try:
            gen = DocxTemplateGenerator(
                template_path=template_path,
                context={"content_text": text},
                output_dir=output_dir,
            )
            result_path = gen.generate(file_name)
            InfoBar.success(self, "Готово", f"Документ сохранён:\n{result_path}")
        except Exception as e:
            InfoBar.error(self, "Ошибка", str(e))


from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget


class DocumentPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Документы")

        layout = QVBoxLayout(self)

        title = TitleLabel("Документы")
        layout.addWidget(title)

        tabs = TabWidget(self)
        tabs.addTab(self._create_list_tab(), "Список")
        tabs.addTab(self._create_add_tab(), "Добавить")
        tabs.addTab(_GenerateTab(), "Создать")
        layout.addWidget(tabs)

    def _create_list_tab(self) -> QWidget:
        columns = [
            ("Тип", "doc_type", 140),
            ("Номер", "doc_number", 120),
            ("Дата", "doc_date", 100),
            ("Название", "title", 250),
            ("Статус", "status", 100),
            ("Создал", "created_by.full_name", 180),
            ("Оборудование", "equipment.name", 180),
        ]
        w = QWidget()
        layout = QVBoxLayout(w)
        self.table = DataTableWidget(Document, columns)
        layout.addWidget(self.table)
        return w

    def _create_add_tab(self) -> QWidget:
        w = QWidget()
        QVBoxLayout(w).addWidget(BodyLabel("Форма добавления документа (в разработке)"))
        return w
