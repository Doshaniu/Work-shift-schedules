from .calendar_utils import generate_month_days, get_day_type
from .employees import Employee
from typing import Dict, List
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

        # Пулы для Д1/Д2 и список тех, кто обязан быть OFF после Д2
        pool_for_shifts, forced_off = get_shift_pools(available_employee, day)

        schedule[day] = {
            "D1": None,
            "D2": None,
            "D": [],
            "OFF": []
        }

        # -----------------------------
        #        ВЫБОР D1
        # -----------------------------
        emp_d1 = choose_employer_for_D1(pool_for_shifts, today=day)

        if emp_d1 is not None:
            if emp_d1 in pool_for_shifts:
                pool_for_shifts.remove(emp_d1)
            if emp_d1 in available_employee:
                available_employee.remove(emp_d1)

            emp_d1.assign_shift("D1", last_shift_date=day)
            schedule[day]["D1"] = emp_d1.name

        # -----------------------------
        #        ВЫБОР D2
        # -----------------------------
        emp_d2 = choose_employer_for_D2(pool_for_shifts, today=day)

        if emp_d2 is not None:
            if emp_d2 in pool_for_shifts:
                pool_for_shifts.remove(emp_d2)
            if emp_d2 in available_employee:
                available_employee.remove(emp_d2)

            emp_d2.assign_shift("D2", last_shift_date=day)
            schedule[day]["D2"] = emp_d2.name

        # -----------------------------
        #     OFF после D2
        # -----------------------------
        for emp in forced_off:
            if emp in available_employee:
                available_employee.remove(emp)

            emp.assign_shift("OFF", last_shift_date=day)
            schedule[day]["OFF"].append(emp.name)

        # DEBUG: показать состояние пулов перед назначением обычных смен
        print(f"[DEBUG] {day}: pool_for_shifts={len(pool_for_shifts)}, available_employee={len(available_employee)}, forced_off={len(forced_off)}")
        print("  available:", [emp.name for emp in available_employee])
        # -----------------------------
        #        Обычные смены D
        # -----------------------------
        if day_type == "workday":
            # Сортируем по наименьшему количеству обычных дней D (чтобы выравнивать D),
            # затем по общему числу дежурств (D1+D2) в качестве тайбрейкера.
            available_employee.sort(
                key=lambda emp: (
                    emp.count_work_days,
                    emp.count_daytime_shifts + emp.count_evening_shifts,
                )
            )

            # Сколько нужно сотрудников на обычный рабочий день
            required = 4

            # Выбираем из доступного пула
            selected: List[Employee] = available_employee[:required]

            # Если не хватает — дозаполним из pool_for_shifts (те, кто не в forced_off),
            # но не возвращаем в выбор тех, кто уже был назначен D1/D2 сегодня.
            if len(selected) < required:
                needed = required - len(selected)
                # emp_d1/emp_d2 may be defined above; if not, use None
                try:
                    already_assigned = {schedule[day]["D1"], schedule[day]["D2"]}
                except Exception:
                    already_assigned = {None}

                # Дополнительно допускаем сотрудников, вернувшихся из отпуска вчера,
                # чтобы они могли получить обычный рабочий день в первый день после отпуска.
                yesterday = day - __import__('datetime').timedelta(days=1)
                returned_yesterday = [e for e in employees.values()
                                       if any(end == yesterday for (start, end) in e.vacations)]

                fillers = [e for e in pool_for_shifts
                           if e.name not in already_assigned and e not in selected]
                # Добавляем вернувшихся вчера, если они ещё не в fillers
                for e in returned_yesterday:
                    if e not in fillers and e not in selected and e in pool_for_shifts:
                        fillers.append(e)
                selected.extend(fillers[:needed])

            print(f"[DEBUG] {day}: selected_for_D = {[e.name for e in selected]}")
            for emp in selected:
                emp.assign_shift("D", last_shift_date=day)
                schedule[day]["D"].append(emp.name)
            print(f"[DEBUG] {day}: schedule D = {schedule[day]['D']}")

        # -----------------------------
        #    Выходные → все OFF
        # -----------------------------
        else:
            for emp in available_employee:
                emp.assign_shift("OFF", last_shift_date=day)
                schedule[day]["OFF"].append(emp.name)

    return schedule
