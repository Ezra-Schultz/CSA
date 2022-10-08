from __future__ import print_function
import math

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_URL = input("Enter spreadsheet URL: ")
SAMPLE_SPREADSHEET_ID = SAMPLE_SPREADSHEET_URL.strip('https://docs.google.com/spreadsheets/d/')[:-11]
SAMPLE_RANGE_NAME = "A2:D30"

def curve(scores: list):
    highest = 0
    for i in scores:
        if i > highest:
            highest = i
    n = math.sqrt(100 - highest)
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
            creds = flow.run_local_server(
                port=8080,
                include_client_id=True,
                api="AIzaSyCeojUyh1_p2E_F_8Mhb3NSI-IX_UEiGYw",
            )
        # Save credentials
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )

        # writeCurve = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='D2:D30')
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        # print("Name, Grade:")
        list_ = []
        for row in values:
            # Print columns A and B, represented by indices A and B.
            # print(f"{row[0]}, {row[1]}")
            row[2] = int(row[2])
            list_.append(row[2])
        print(list_)
        list_ = curve(list_)
        list_ = [int(i) for i in list_]
        print(list_)
        _list_ = []
        for i in range(len(values)):
            # Print columns A and E, which correspond to indices 0 and 4.
            # print('%s %s: %s, %s' % (i[0][0], i[1][0], i[2][0], list_))
            _list_.append(values[i][2])
        print(_list_)

    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
