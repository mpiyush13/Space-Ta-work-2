import gspread
import pandas as pd

SHEET_ID = '1pbTLKnkCcDuMIoejs_mWW8SnZVW5_Eqgk2Qs1oZgQqk'
SHEET_NAME = 'Student Data'
gc = gspread.service_account('keys.json')
spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)
rows = worksheet.get_all_records()
print(rows[:5])

print('==============================')
df = pd.DataFrame(rows)
print(df.head())