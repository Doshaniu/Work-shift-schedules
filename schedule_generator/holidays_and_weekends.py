from datetime import date

from constants import HOLIDAYS, WEEKENDS

def is_holiday(d: date) -> bool:
    """Проверка является ли текущая дата праздником."""
    return d in HOLIDAYS

def is_weekend(d: date) -> bool:
    """Проверка является ли текущая дата выходным."""
    return d.weekday() in WEEKENDS

def is_day_off(d: date) -> bool:
    """Возвращает True, если дата праздничный или выходной день."""
    return is_holiday(d) or is_weekend(d)