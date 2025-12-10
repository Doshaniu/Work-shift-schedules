from datetime import date
from pprint import pprint

from .parse_vacations_days import parsed_vacations_days

class Employee:
    """Класс работника."""
    def __init__(self, name: str):
        self.name = name
        self.vacations: list[tuple[date, date]] = [] # Хранит список кортежей с датами отпусков.

        self.count_daytime_shifts: int = 0 # Хранит количество дневных дежурств. D1.
        self.count_evening_shifts: int = 0 # Хранит количество вечерних дежурств. D2.
        self.count_work_days:int = 0 # Хранит количество отработанных обычных дней. D.

        self.last_shift: str | None = None # Последняя отработанная смена.
        self.last_shift_date: date | None = None # Дата последней смены.

    def add_vacation(self, start: date, end: date) -> None:
        """Добавляем отпускные дни работника."""
        self.vacations.append((start, end))

    def is_on_vacation(self, d: date) -> bool:
        """Проверка находится ли работник в отпуске."""
        for start, end in self.vacations:
            if start <= d <= end:
                return True
        return False

    def assign_shift(self, shift: str, last_shift_date: date) -> None:
        """Выставляем последнюю отработанную смену работнику."""
        if shift == "D1":
            self.count_daytime_shifts += 1
        elif shift == "D2":
            self.count_evening_shifts += 1
        elif shift == "D":
            self.count_work_days += 1
        self.last_shift = shift
        self.last_shift_date = last_shift_date


def create_employees(vacation_dict: dict) -> dict:
    """Создаем работников и добавляем им даты отпусков."""
    employees = {}
    for name, vacation_data in vacation_dict.items():
        employee = Employee(name)
        for start, end in vacation_data:
            employee.add_vacation(start, end)
        employees[name] = employee
    return employees

vacation_dict = parsed_vacations_days()
employees_data = create_employees(vacation_dict)