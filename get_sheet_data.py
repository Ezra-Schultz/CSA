from __future__ import print_function

# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gspread'])
import gspread
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# The ID and range of a sample spreadsheet.
SPREADSHEET_URL = input("Enter spreadsheet URL: ")

# SAMPLE_SPREADSHEET_ID = '1d0hwrPTGWjzQ60HL6bBy2olGi-lg20aozqeEWTM0Gjw'
SAMPLE_RANGE_NAME = "A1:C30"


def curve(scores: list):
    highest = 0
    for i in scores:
        if i > highest:
            highest = i
    n = 100 - highest
    scores = [i + n for i in scores]
    return scores


# noinspection PyUnresolvedReferences
def main():
    """
    Imports data from a spreadsheet and pushes it to Google Classroom
    """
    creds = None
    # noinspection PyUnresolvedReferences
    if not creds or not creds.valid:
        # noinspection PyUnresolvedReferences
        if creds and creds.expired and creds.refresh_token:
            # noinspection PyUnresolvedReferences
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            # Local server for logging in to Google account
            creds = flow.run_local_server(port=8080, include_client_id=True)

    try:
        client = gspread.authorize(creds)
        sheet = client.open_by_url(SPREADSHEET_URL).sheet1

        range_ = sheet.range('A1:C30')
        print(range_)
        format_list = []
        for j in range(3):
            temp_list = []
            for i in range(len(range_)):
                if i % 3 == j:
                    temp_list.append(range_[i].value)
            format_list.append(temp_list)
        [print(i) for i in format_list]
        grades = format_list[2][1:]
        grades = [int(i) for i in grades]
        curves = curve(grades)
        for i in range(len(curves)):
            sheet.update_cell(i + 1, 4, curves[i])

    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
