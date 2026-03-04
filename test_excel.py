"""Test model's ability to work with Excel data."""

import sys
import openpyxl
from openai import OpenAI

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/v1"
EXCEL_FILE = sys.argv[2] if len(sys.argv) > 2 else None

if not EXCEL_FILE:
    print("Usage: python test_excel.py <RUNPOD_URL> <excel_file.xlsx>")
    print("Example: python test_excel.py http://your-pod-ip:8000/v1 data.xlsx")
    sys.exit(1)

# Read Excel file
wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)

sheets_data = {}
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    rows = []
    for row in ws.iter_rows(values_only=True):
        rows.append([str(cell) if cell is not None else "" for cell in row])
    sheets_data[sheet_name] = rows

# Format as text for the model
excel_text = ""
for sheet_name, rows in sheets_data.items():
    excel_text += f"\n=== Sheet: {sheet_name} ===\n"
    for row in rows[:100]:  # limit to first 100 rows
        excel_text += " | ".join(row) + "\n"

print(f"Loaded {len(sheets_data)} sheets, sending to model...")

client = OpenAI(base_url=BASE_URL, api_key="not-needed")
models = client.models.list()

response = client.chat.completions.create(
    model=models.data[0].id,
    messages=[
        {
            "role": "system",
            "content": "You are a data analyst. Analyze the provided Excel data carefully.",
        },
        {
            "role": "user",
            "content": f"Here is the Excel data:\n{excel_text}\n\nОпиши структуру данных, что в них содержится, и какие выводы можно сделать.",
        },
    ],
    max_tokens=2048,
    temperature=0.3,
)

print("\nModel response:")
print(response.choices[0].message.content)
