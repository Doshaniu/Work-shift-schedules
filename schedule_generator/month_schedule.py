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

        # Пулы для Д1/Д2 и список тех, кто обязан быть OFF после Д2.
        pool_for_shifts, forced_off = get_shift_pools(available_employee, day)

        schedule[day] = {
            "D1": None,
            "D2": None,
            "D": [],
            "OFF": []
        }

        emp_d1 = choose_employer_for_D1(pool_for_shifts, today=day)

        if emp_d1 is not None:
            if emp_d1 in pool_for_shifts:
                pool_for_shifts.remove(emp_d1)
            if emp_d1 in available_employee:
                available_employee.remove(emp_d1)

            emp_d1.assign_shift("D1", last_shift_date=day)
            schedule[day]["D1"] = emp_d1.name

        emp_d2 = choose_employer_for_D2(pool_for_shifts, today=day)

        if emp_d2 is not None:
            if emp_d2 in pool_for_shifts:
                pool_for_shifts.remove(emp_d2)
            if emp_d2 in available_employee:
                available_employee.remove(emp_d2)

            emp_d2.assign_shift("D2", last_shift_date=day)
            schedule[day]["D2"] = emp_d2.name

        # Проставляем выходные тем, кто вчера был на Д2.
        for emp in forced_off:
            if emp in available_employee:
                available_employee.remove(emp)

            emp.assign_shift("OFF", last_shift_date=day)
            schedule[day]["OFF"].append(emp.name)

        if day_type == "workday":
            # Сортируем по наименьшему количеству обычных дней Д,
            # затем по общему числу дежурств (Д1+Д2).
            available_employee.sort(
                key=lambda emp: (
                    emp.count_work_days,
                    emp.count_daytime_shifts + emp.count_evening_shifts,
                )
            )

            # Назначаем всех оставшихся на обычные рабочие дни.
            for emp in available_employee:
                emp.assign_shift("D", last_shift_date=day)
                schedule[day]["D"].append(emp.name)

        # Если выходной, всем кто не в смене/отпуске ставим OFF
        else:
            for emp in available_employee:
                emp.assign_shift("OFF", last_shift_date=day)
                schedule[day]["OFF"].append(emp.name)

    return schedule
