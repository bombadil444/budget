from datetime import date
from google.oauth2.service_account import Credentials
from gspread import authorize
import os


def ensure_root_cwd():
    """Changes the current working directory (CWD) to the root of the repository."""
    script_path = os.path.realpath(__file__)
    root_dir = os.path.dirname(os.path.dirname(script_path))
    os.chdir(root_dir)


def get_date_str():
    today = date.today()
    year = today.year
    month = today.month - 1

    date_str = f"{year:04d}{month:02d}"
    return date_str


ensure_root_cwd()

spreadsheet_id = "1GlWr5yCJkLPt4fpiVcM3gWUWV0zp7o6oRj4ioI-VVtE"
sheet_name = "Budget"

# read credentials and authorize gspread
creds = Credentials.from_service_account_file(
    "creds.json",
    scopes=[
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ],
)
client = authorize(creds)
