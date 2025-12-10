from datetime import date, timedelta
from typing import Dict, List, Tuple

from .employees import Employee


def get_available_employees(
        employees: Dict[str, Employee],
        day: date
) -> List[Employee]:
    """Работники, которые НЕ в отпуске."""
    return [emp for emp in employees.values() if not emp.is_on_vacation(day)]


def get_shift_pools(
        available_employees: List[Employee],
        today: date
) -> Tuple[List[Employee], List[Employee]]:
    """После Д2 обязателен OFF."""
    forced_off = [
        emp for emp in available_employees
        if emp.last_shift == "D2"
        and emp.last_shift_date == (today - timedelta(days=1))
    ]

    pool_for_shifts = [
        emp for emp in available_employees if emp not in forced_off
    ]

    return pool_for_shifts, forced_off


def can_work_shift(emp: Employee, today: date, shift: str) -> bool:
    """Правила допуска к смене для конкретного сотрудника на дату `today`."""
    # Если нет информации о предыдущей смене — разрешаем
    if not emp.last_shift or not emp.last_shift_date:
        return True

    yesterday = today - timedelta(days=1)

    if emp.last_shift_date == yesterday and emp.last_shift == "D2":
        return False if shift in ("D1", "D2", "D") else True

    # Если вчера была D1 — сегодня разрешена только обычная смена D.
    if emp.last_shift_date == yesterday and emp.last_shift == "D1":
        return shift == "D"

    # Если вчера была обычная смена D — сегодня можно любую смену.
    if emp.last_shift_date == yesterday and emp.last_shift == "D":
        return True

    # Запрет на повтор той же дежурной смены два дня подряд.
    if (
            emp.last_shift_date == yesterday
            and shift in ("D1", "D2")
            and emp.last_shift == shift
    ):
        return False

    return True


def choose_employer_for_D1(
        available_employees: List[Employee],
        today: date
) -> Employee | None:

    candidates = [
        emp for emp in available_employees
        if can_work_shift(emp, today, "D1")
        ]
    if not candidates:
        return None
    # Приоритеты для D1:
    # 1) минимизировать число дневных дежурств (D1)
    # 2) вторично минимизировать число вечерних дежурств (D2)
    # 3) затем минимизировать число обычных рабочих дней
    return min(
        candidates,
        key=lambda emp: (
            emp.count_daytime_shifts,
            emp.count_evening_shifts,
            emp.count_work_days,
        ),
    )


def choose_employer_for_D2(
        available_employees: List[Employee],
        today: date
) -> Employee | None:

    candidates = [
        emp for emp in available_employees
        if can_work_shift(emp, today, "D2")
    ]
    if not candidates:
        return None
    # Приоритеты для D2:
    # 1) минимизировать число вечерних дежурств (D2)
    # 2) вторично минимизировать число дневных дежурств (D1)
    # 3) затем минимизировать число обычных рабочих дней
    return min(
        candidates,
        key=lambda emp: (
            emp.count_evening_shifts,
            emp.count_daytime_shifts,
            emp.count_work_days,
        ),
    )
