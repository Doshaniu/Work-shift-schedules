from datetime import date, timedelta
from .constants import NEW_YEAR_START_DAY
from typing import List
from .holidays_and_weekends import is_holiday, is_weekend


def generate_month_days(year: int, month: int) -> List[date]:
    """Генерирует список дат для указанного месяца.
        Для января стартует с 12 числа, для остальных с 1."""
    if month == 1:  # Если месяц январь.
        start_day = NEW_YEAR_START_DAY
    else:
        start_day = 1  # В ином случае начинаем с 1 числа текущего месяца.
    d = date(year, month, start_day)
    days = []
    while d.month == month:
        days.append(d)
        d += timedelta(days=1)
    return days


def get_day_type(d: date) -> str:
    if is_holiday(d):
        return "holiday"
    if is_weekend(d):
        return "weekend"
    return "workday"
