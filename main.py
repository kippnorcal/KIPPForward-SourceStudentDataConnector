from os import getenv
import pygsheets
from sqlsorcery import MSSQL


def fetch_view_data():
    client = pygsheets.authorize(service_file='./service_account_cred.json')
    sheet = client.open_by_key(getenv('SHEET_KEY'))
    worksheet = sheet.worksheet_by_title('All Students - Test')
    return worksheet


def get_worksheet():
    pass


def compare_view_data_to_sheets():
    pass


def trim_sheets_data():
    # best thing would be to take teh number of rows, subtract difference to get starting point
    # from starting point, clear columns A to S; number of iterations == difference
    pass

def truncate_and_reload():
    pass


# access sheet
# pull view data
# if length df != sheets
#       delete difference from worksheet
# trunc and reload to All Students - Test


if __name__ == '__main__':
    print_hi('PyCharm')
