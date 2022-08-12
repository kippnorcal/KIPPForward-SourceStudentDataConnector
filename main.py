import logging
from os import getenv
from sys import stdout
import traceback

from pandas import DataFrame
from pygsheets import authorize
from pygsheets import worksheet
from sqlsorcery import MSSQL

from mailer import Mailer

logging.basicConfig(
    handlers=[
        logging.FileHandler(filename="./app.log", mode="w+"),
        logging.StreamHandler(stdout),
    ],
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p %Z",
)


def fetch_worksheet() -> worksheet:
    logging.info('Accessing Googlesheets Data')
    client = authorize(service_file='./service_account_cred.json')
    sheet = client.open_by_key(getenv('SHEET_KEY'))
    wksheet = sheet.worksheet_by_title('All Students - Test')
    return wksheet


def fetch_view_data() -> DataFrame:
    logging.info('Running view SQL statement')
    sql = MSSQL()
    return sql.query_from_file('./sql/KTC_Match_Tracker_Students.sql')


def compare_view_data_to_sheets(view_data: DataFrame, sheet_data: worksheet):
    sheet_data_df = sheet_data.get_as_df(start="A1", end=(1000, 1), include_tailing_empty_rows=False)
    logging.info(f'Sheets has {len(sheet_data_df.index)} records. View returned {len(view_data.index)} records')
    return len(sheet_data_df) - len(view_data), len(sheet_data_df) + 2


def trim_sheets_data(last_row: int, rows: int, wksheet: worksheet) -> None:
    # best thing would be to take teh number of rows, subtract difference to get starting point
    # from starting point, clear columns A to S; number of iterations == difference
    start = last_row - (rows + 2)
    start = f'A{start}'
    end = f'S{last_row}'
    logging.info(f'Clearing cells from {start} to {end}')
    wksheet.clear(start, end)


def truncate_and_reload(wksheet: worksheet, df: DataFrame) -> None:
    logging.info(f'Truncate and reloaded {len(df.index)}')
    df.fillna("", inplace=True)
    wksheet.set_dataframe(df, "A2", copy_head=False)


def main():
    view_df = fetch_view_data()
    wksheet_obj = fetch_worksheet()
    diff, start_row = compare_view_data_to_sheets(view_df, wksheet_obj)
    if diff > 0:
        logging.info("Trimming Googlesheet Data")
        trim_sheets_data(start_row, diff, wksheet_obj)
    truncate_and_reload(wksheet_obj, view_df)


if __name__ == '__main__':
    mailer = Mailer("Google Sheets - Source Student Data")
    try:
        main()
        mailer.notify()
    except Exception:
        mailer.notify(error_message=traceback.TracebackException)
