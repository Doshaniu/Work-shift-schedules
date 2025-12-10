from datetime import date

import pandas as pd
from pandas import ExcelWriter

from schedule_generator.month_schedule import generate_month_shift_schedule
from schedule_generator.employees import employees_data
from schedule_generator.constants import YEAR, WEEKDAYS, QUANTITY_OF_WORKING_HOURS, MONTH_TO_NUMBER, XLSX_PATH
from schedule_generator.styles import apply_style



def add_summary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Добавляет столбцы Кол-во часов, Д1, Д2, Рб.д, Итого."""
    day_cols = [col for col in df.columns if isinstance(col, int)]
    df["Д1"] = df[day_cols].apply(lambda row: sum(1 for x in row if x == "Д1"), axis=1)
    df["Д2"] = df[day_cols].apply(lambda row: sum(1 for x in row if x == "Д2"), axis=1)
    df["Рб.д"] = df[day_cols].apply(lambda row: sum(1 for x in row if x == "Д"), axis=1)
    df["Итого"] = df[["Д1", "Д2", "Рб.д"]].sum(axis=1)
    df["Кол-во часов"] = df['Итого'] * QUANTITY_OF_WORKING_HOURS
    return df

def add_weekday_header(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    day_cols = [col for col in df.columns if isinstance(col, int)]
    weekday_row = [""]  # Сдвиг на одну ячейку под колонку "Сотрудник".

    # Дни недели под датами.
    for day in day_cols:
        d = date(year, month, day)
        weekday_row.append(WEEKDAYS[d.weekday()])

    # Сколько итоговых столбцов справа.
    summary_cols_count = len(df.columns) - (1 + len(day_cols))
    weekday_row.extend([""] * summary_cols_count)

    # собираем
    weekday_df = pd.DataFrame([weekday_row], columns=df.columns)
    df = pd.concat([weekday_df, df], ignore_index=True)
    return df



def schedule_to_table(schedule: dict, employees: dict, year: int, month: int) -> pd.DataFrame:
    """
    Превращает schedule в таблицу формата как в примере.
    """
    # Подготовка пустой структуры
    table = {}

    # Имена сотрудников — строки
    for emp in employees.values():
        table[emp.name] = {}

    # Заполняем по дням
    for day, shifts in schedule.items():
        day_num = day.day

        # D1
        if shifts["D1"]:
            table[shifts["D1"]][day_num] = "Д1"

        # D2
        if shifts["D2"]:
            table[shifts["D2"]][day_num] = "Д2"

        # D (обычная смена)
        for name in shifts["D"]:
            table[name][day_num] = "Д"

        # OFF
        for name in shifts["OFF"]:
            table[name][day_num] = "В"

    # Заполняем пустые значения (если у сотрудника не было смены)
    max_days = max(d.day for d in schedule.keys())
    for emp in table:
        for d in range(1, max_days + 1):
            table[emp].setdefault(d, "")

    # Преобразуем в DataFrame
    df = pd.DataFrame.from_dict(table, orient="index")
    df.insert(0, "Сотрудник", df.index)
    date_cols = sorted([c for c in df.columns if isinstance(c, int)])
    df = df[["Сотрудник"] + date_cols]

    return df



def save_to_excel(schedule: dict, filename: str):
    df = schedule_to_table(schedule, employees_data, year=YEAR, month=MONTH)
    df = add_summary_columns(df)
    df = add_weekday_header(df, YEAR, MONTH)

    sheet_name = f'{MONTH_TO_NUMBER[MONTH]}_{YEAR}'
    XLSX_PATH.mkdir(parents=True, exist_ok=True)
    filepath = XLSX_PATH / filename
    mode = "a" if filepath.exists() else "w"

    with ExcelWriter(filepath, mode=mode, engine="openpyxl", if_sheet_exists="replace") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        apply_style(writer, sheet_name)

MONTH = 12

schedule = generate_month_shift_schedule(year=YEAR, month=MONTH, employees=employees_data)
save_to_excel(schedule, filename=f"График_работ_2026.xlsx")