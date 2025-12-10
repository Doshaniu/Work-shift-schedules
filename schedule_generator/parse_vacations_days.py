from datetime import date, datetime
from pathlib import Path
import pandas as pd


project_dir = Path(__file__).parent.parent

file_path = project_dir / 'input_data' / 'отпуск_2026_ТЗ.xlsx'


df = pd.read_excel(file_path, index_col=0)

def parse_data_string(period: str) -> tuple[date, date]:
    """Парсим строку даты в кортеж."""
    start_date, end_date = period.split('-')
    start_date = datetime.strptime(start_date.strip(), '%d.%m.%Y').date()
    end_date = datetime.strptime(end_date.strip(), '%d.%m.%Y').date()
    return (start_date, end_date)

def parse_cell_value(value: str) -> list[tuple[date, date]]:
    """Если в одной ячейке несколько значений."""
    periods = value.split('\n')
    result = [parse_data_string(period) for period in periods]
    return result

def parsed_vacations_days():
    """Парсим дату из exel файла."""
    result = {}
    for index, row in df.iterrows():
        employee_vacations = []
        for month_name, value in row.items():
            if pd.notna(value):
                employee_vacations.extend(parse_cell_value(value))
        result[index] = employee_vacations
    return  result
