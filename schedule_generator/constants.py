from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

HOLIDAYS = {
    date(2026, 1, 1),
    date(2026, 1, 2),
    date(2026, 1, 3),
    date(2026, 1, 4),
    date(2026, 1, 5),
    date(2026, 1, 6),
    date(2026, 1, 7),
    date(2026, 1, 8),
    date(2026, 1, 9),
    date(2026, 2, 23),
    date(2026, 3, 8),
    date(2026, 5, 1),
    date(2026, 5, 9),
    date(2026, 5, 10),
    date(2026, 5, 11),
    date(2026, 6, 12),
    date(2026, 11, 4),
}
"""Праздничные дни 2026 года."""

WEEKENDS = (5, 6)
"""Выходные дни."""

NEW_YEAR_START_DAY = 12
"""Начало рабочего года с 12 января."""

WEEKDAYS = ['Пнд', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

YEAR = 2026

QUANTITY_OF_WORKING_HOURS = 8
"""Количество рабочих часов в день."""

MONTH_TO_NUMBER = {
    1 : "Январь",
    2 : "Февраль",
    3 : "Март",
    4 : "Апрель",
    5 : "Май",
    6 : "Июнь",
    7 : "Июль",
    8 : "Август",
    9 : "Сентябрь",
    10 : "Октябрь",
    11 : "Ноябрь",
    12 : "Декабрь",
}

XLSX_PATH = BASE_DIR / "output_data"