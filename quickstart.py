from __future__ import print_function

import os.path
import gspread

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_URL = input("Enter spreadsheet URL: ")
SAMPLE_SPREADSHEET_ID = SAMPLE_SPREADSHEET_URL.strip(
    "https://docs.google.com/spreadsheets/d/"
)[:-11]
SAMPLE_RANGE_NAME = "A1:D30"


def curve(scores: list):
    highest = 0
    for i in scores:
        if i > highest:
            highest = i
    n = 100 - highest
    scores = [i + n for i in scores]
    return scores


def main():
    """
    Imports data from a spreadsheet and pushes it to Google Classroom
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            # Local server for logging in to Google account
            creds = flow.run_local_server(port=8080, include_client_id=True)

        # Save credentials
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # service = build("sheets", "v4", credentials=creds)

        # sheet = service.spreadsheets()
        client = gspread.authorize(creds)
        sheet = client.open("Grades").sheet1

        # writeCurve = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='D2:D30')
        count = 1
        lst = []
        while sheet.row_values(count) != []:
            values = sheet.row_values(count)
            lst.append(values)
            count += 1
        print(lst)
        # if not values:
        # print("No data found.")
        # return
        cells = sheet.range(SAMPLE_RANGE_NAME)
        print([cell.value for cell in cells])
        for i in range(0, len(cells), 4):
            yield cells[i : i + 4]

        # curveGrades = curve([int(row[2]) for row in values])
        # sheet.update_acell(4, 2, curveGrades[1])
        for i in range(len(values)):
            data = values[i]
            print(
                f"{data[0]} {data[1]} -> grade: {data[2]}"
            )

    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
