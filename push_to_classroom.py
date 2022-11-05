from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# from jsonrpcclient import requests

# import requests
# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.coursework.me'
]


def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080)

    try:
        service = build('classroom', 'v1', credentials=creds)

        # Call the Classroom API
        # results = service.courses().list(pageSize=10).execute()
        id_ = service.courses().list(pageSize=10).execute().get('courses', [])[0]['id']
        studentList = service.courses().students().list(courseId=id_).execute().get('students', [])
        if not id_:
            print('No courses found.')
            return
        # Prints the names of the first 10 courses.
        # print('Courses:')
        # for student in studentList:
        #     print(f"{student['profile']['name']['fullName']}, {student['profile']['id']}")
        print(service.courses().list().execute())
        print(studentList[input('n = ')]['courseId'])

        studentSubmission = {
            'assignedGrade': 99,
            'draftGrade': 80
        }
        service.courses().courseWork().studentSubmissions().patch(courseId='503892896755', courseWorkId='491585441102', id='Cg4ItKCJk9UOEM6amqanDg', updateMask='assignedGrade,draftGrade', body=studentSubmission).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
