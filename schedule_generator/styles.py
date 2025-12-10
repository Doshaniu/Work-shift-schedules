from dateutil.rrule import weekday
from openpyxl.styles import PatternFill, Alignment
from openpyxl.utils import get_column_letter

GRAY = PatternFill(start_color="C0C0C0", end_color="C0C0C0", fill_type="solid")

def apply_style(writer, sheet_name):
    ws = writer.book[sheet_name]

    weekday_row = 2
    for col in range(2, ws.max_column + 1):
        cell = ws.cell(row=weekday_row,  column=col)
        if cell.value in ("Сб", "Вс"):
            cell.fill = GRAY
            ws.cell(row=2, column=col).fill = GRAY

    for row in range(3, ws.max_row + 1):
        for col in range(2, ws.max_column + 1):
            if ws.cell(row=row, column=col).value == "В":
                ws.cell(row=row, column=col).fill = GRAY