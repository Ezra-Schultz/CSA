from __future__ import print_function
import math

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", 'https://www.googleapis.com/auth/classroom.courses.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_URL = input("Enter spreadsheet URL: ")
SAMPLE_SPREADSHEET_ID = SAMPLE_SPREADSHEET_URL.strip('https://docs.google.com/spreadsheets/d/')[:-11]
SAMPLE_RANGE_NAME = "A1:B29"

def curve(value: int):
    
    i_min = 0
    i_max = 100
    o_min = 0
    o_max = 100

    a = pow(value - i_min, 2)
    b = pow(i_max - i_min, 2)
    c = pow(value - o_max, 2)
    d = pow(o_max - o_min, 2)
    final = ((a / b) + (c / d))
    print(a, b, c, d, final)
    return final

x = 0
print(curve(x))



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
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        print("Name, Grade:")
        for row in values:
            # Print columns A and B, represented by indices A and B.
            print(f"{row[0]}, {row[1]}")
    except HttpError as err:
        print(err)


# if __name__ == "__main__":
    # main()
