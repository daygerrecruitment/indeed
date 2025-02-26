import os
from dotenv import load_dotenv

load_dotenv()
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")
print(SPREADSHEET_URL)
