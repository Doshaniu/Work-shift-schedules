from datetime import date, timedelta
from typing import List, Dict, Tuple

from .employees import Employee


def get_available_employees(
        employees: Dict[str, Employee],
        day: date
        ) -> List[Employee]:
    """Получаем список работников, которые не в отпуске в указанную дату."""
    result = []
    for employer in employees.values():
        if not employer.is_on_vacation(day):
            result.append(employer)
    return result


def get_shift_pools(
        available_employees: List[Employee],
        today: date
        ) -> Tuple[List[Employee], List[Employee]]:
    """Принудительный выходной для работника после ночной смены."""
    forced_off = [
        emp for emp in available_employees
        if emp.last_shift == "D2"
        and emp.last_shift_date == (today - timedelta(days=1))
    ]
    pool_for_shifts = [
        emp for emp in available_employees if emp not in forced_off
    ]
    return pool_for_shifts, forced_off


def can_work_shift_today(employee: Employee, today: date) -> bool:
    """Проверка может ли сотрудник работать сегодня(Вчера не D2)"""
    if employee.last_shift == "D2" and employee.last_shift_date:
        yesterday = today - timedelta(days=1)
        if employee.last_shift_date == yesterday:
            return False
    return True


def choose_employer_for_D1(available_employees: List[Employee]) -> Employee | None:
    """Выбираем кандидата на дневную смену по количеству дневных смен."""
    candidate_employees = [emp for emp in available_employees]

    if not candidate_employees:
        return None

    return min(candidate_employees,
            key=lambda emp:(
                    emp.count_daytime_shifts + emp.count_evening_shifts,
                    emp.count_work_days)
                )

def choose_employer_for_D2(available_employees: List[Employee], today: date) -> Employee | None:
    """Выбираем кандидата на вечернюю смену по количеству смен и доступности."""
    candidate_employees = [emp for emp in available_employees if can_work_shift_today(emp, today)]

    if not candidate_employees:
        return None
    return min(candidate_employees,
               key=lambda emp: (
                   emp.count_daytime_shifts + emp.count_evening_shifts,
                   emp.count_work_days)
               )
