# Equipment Accounting System

Desktop-приложение для учёта оборудования, документов, перемещений, обслуживания и сетевой инфраструктуры учебного центра.

## Stack

| Компонент | Технология |
|---|---|
| GUI | PyQt6 + qfluentwidgets (Fluent Design) |
| ORM | SQLAlchemy 2.0 |
| БД | SQLite (WAL + foreign keys) |
| Валидация | Pydantic v2 |
| Документы | python-docx / docxtpl (DOCX), ReportLab (PDF) |
| Excel | pandas / openpyxl |
| Сборка | PyInstaller |

## Структура проекта

```
project/
├── main.py                 # Точка входа
├── config/                 # Подключение к БД (SQLAlchemy engine, session)
├── database/
│   ├── models/             # 10 ORM-моделей (Location, Employee, Equipment, ...)
│   ├── schemas/            # Pydantic-схемы (Create/Read DTO)
│   └── repository.py       # Generic CRUD BaseRepository[T]
├── pages/                  # UI-страницы (10 шт.)
│   ├── main/index.py       # Главное окно + навигация
│   ├── dashboard/          # Панель со статистикой, графиками, алертами
│   ├── equipment/          # Оборудование
│   ├── employee/           # Сотрудники
│   ├── location/           # Локации
│   ├── document/           # Документы (список + генерация DOCX)
│   ├── movement/           # Перемещения
│   ├── maintenance/        # Обслуживание
│   ├── inventory/          # Инвентаризация
│   ├── network/            # Сеть (узлы + соединения)
│   └── write_off/          # Списание
├── ui/
│   ├── components/         # Переиспользуемые виджеты (таблицы, графики, фильтры)
│   └── settings/           # Настройки окна (масштаб, тема, fullscreen)
├── utillities/             # Утилиты
│   ├── useTables.py        # DataTableWidget — таблицы с фильтрацией
│   ├── animations.py       # Анимации (счётчики, fade-in, прогресс-бары)
│   ├── excel_import/       # Импорт Excel
│   └── pdf_generation/     # Генерация DOCX/PDF
├── docs/                   # DOCX-шаблоны
└── seed_data.py            # Заполнение БД тестовыми данными
```

## Модели данных

Всего 10 таблиц, связанных внешними ключами:

- **Locations** — помещения/локации (здание, этаж, кабинет, тип)
- **Employees** — сотрудники (ФИО, должность, отдел, контакты)
- **Equipment** — оборудование (инв. номер, категория, статус, стоимость, гарантия, локация, ответственный)
- **Documents** — документы (тип, номер, дата, файл, статус, создатель)
- **EquipmentMovements** — перемещения (откуда → куда, дата, причина, основание)
- **MaintenanceRecords** — ТО (тип, статус, дата, исполнитель, стоимость)
- **WriteOffActs** — акты списания (номер, причина, решение, комиссия)
- **InventoryChecks / Items** — инвентаризации (даты, статус, позиции с ожидаемым/фактическим статусом)
- **NetworkNodes / Links** — сетевая инфраструктура (коммутаторы, маршрутизаторы, соединения)

## Как запустить

```bash
pip install -r requirements.txt
python main.py
```

Для заполнения БД тестовыми данными:

```bash
python seed_data.py
```

## Сборка .exe

```bash
python build.py
```

Готовый исполняемый файл: `dist/EquipmentAccounting/EquipmentAccounting.exe`

## Функции

- 📊 **Панель управления** — анимированные счётчики, кольцевые и столбчатые диаграммы, алерты
- 🔍 **Таблицы** с поиском, фильтрацией, цветовой индикацией статусов
- 🌓 **Переключение темы** (светлая / тёмная / системная)
- 📄 **Генерация документов** из DOCX-шаблонов
- 📏 **Масштабирование**, полноэкранный режим (F11), always-on-top
- 📥 **Импорт из Excel** (расписания)
