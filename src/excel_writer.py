from openpyxl import Workbook, load_workbook


def write_rows(path, headers, rows):
    if path.exists():
        wb = load_workbook(path)
        ws = wb.active
    else:
        path.parent.mkdir(exist_ok=True)
        wb = Workbook()
        ws = wb.active
        ws.append(headers)

    # Keep the Aadhaar number as text so Excel doesn't turn it into a number.
    col = headers.index("Aadhaar Number")
    for row in rows:
        ws.append(row)
        ws.cell(row=ws.max_row, column=col + 1).number_format = "@"
    wb.save(path)
