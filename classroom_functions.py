from enum import Enum
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.coursework.me'
]


class AType(Enum):
    ASSIGNMENT = 0
    SHORT_ANSWER_QUESTION = 1
    LONG_ANSWER_QUESTION = 2
class AState(Enum):
    PUBLISHED = 0
    DRAFT = 1


class AssignmentManager:
    def __init__(self):
        self.flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        self.creds = self.flow.run_local_server(port=8080)
        self.service = build('classroom', 'v1', credentials=self.creds)

    def post_assignment(self, course_id: int, title: str, description: str, links: list, assignment_type=AType.ASSIGNMENT, state=AState.PUBLISHED):
        try:
            newCourseWork = {
                'title': title,
                'description': description,
                'materials': links,
                'workType': assignment_type,
                'state': state,
            }

            newCourseWork = self.service.courses().courseWork().create(
                courseId=course_id, body=newCourseWork).execute()

        except HttpError as error:
            print('An error occurred: %s' % error)

    def select_course(self):
        courses = self.service.courses().list(pageSize=10).execute().get('courses', [])
        for i in courses:
            print(f'{i.get("name")}')
        selectedClass = courses[int(input('enter class index:'))]
        return courses
