import os
from dotenv import load_dotenv

load_dotenv()
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")
CHROME_PATH = os.path.expanduser("~/.config/google-chrome")
CHROME_PROFILE = "Profile 8"