from .calendar_utils import generate_month_days, get_day_type
from .employees import Employee
from typing import Dict
from .shifts import (
    get_available_employees,
    choose_employer_for_D1,
    choose_employer_for_D2,
    get_shift_pools
)


def generate_month_shift_schedule(
        year: int,
        month: int,
        employees: Dict[str, Employee]
        ):
    days = generate_month_days(year, month)
    schedule: dict = {}

    for day in days:
        available_employee = get_available_employees(employees, day)
        day_type = get_day_type(day)
        pool_for_shifts, forced_off = get_shift_pools(available_employee, day)
        schedule[day] = {
            "D1": None,
            "D2": None,
            "D": [],
            "OFF": []
        }
        emp_d1 = choose_employer_for_D1(pool_for_shifts)
        # Убираем выбранного сотрудника из доступных для D2.
        if emp_d1 is not None:
            try:
                pool_for_shifts.remove(emp_d1)
            except ValueError:
                pass
            try:
                available_employee.remove(emp_d1)
            except ValueError:
                pass
            emp_d1.assign_shift(shift="D1", last_shift_date=day)
            schedule[day]["D1"] = emp_d1.name

        emp_d2 = choose_employer_for_D2(pool_for_shifts, today=day)
        # Убираем выбранного сотрудника из доступных для D1.
        if emp_d2 is not None:
            try:
                pool_for_shifts.remove(emp_d2)
            except ValueError:
                pass
            try:
                available_employee.remove(emp_d2)
            except ValueError:
                pass
            emp_d2.assign_shift(shift="D2", last_shift_date=day)
            schedule[day]["D2"] = emp_d2.name

        for emp in forced_off:
            emp.assign_shift(shift="OFF", last_shift_date=day)
            schedule[day]["OFF"].append(emp.name)
            try:
                available_employee.remove(emp)
            except ValueError:
                pass

        if day_type == "workday":
            for emp in available_employee:
                emp.assign_shift(shift="D", last_shift_date=day)
                schedule[day]["D"].append(emp.name)

        else:
            for emp in available_employee:
                emp.assign_shift(shift="OFF", last_shift_date=day)
                schedule[day]["OFF"].append(emp.name)

    return schedule
