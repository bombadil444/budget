from datetime import date
from google.oauth2.service_account import Credentials
from gspread import authorize
import os


def ensure_root_cwd():
    script_path = os.path.realpath(__file__)
    root_dir = os.path.dirname(os.path.dirname(script_path))
    os.chdir(root_dir)


def get_date_str():
    today = date.today()
    year = today.year
    month = today.month - 1

    date_str = f"{year:04d}{month:02d}"
    return date_str


def init_google_sheet():
    ensure_root_cwd()

    # read credentials and authorize gspread
    creds = Credentials.from_service_account_file(
        "creds.json",
        scopes=[
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    client = authorize(creds)

    return client
