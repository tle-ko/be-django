import enum

from drf_yasg.utils import swagger_auto_schema


auto_schema = swagger_auto_schema


class Tags(enum.Enum):
    AUTH = 'Authentication & Verification'
    CREW = 'Crew'
    CREW_ACTIVITY = 'Crew Activity'
    CREW_APPLICATION = 'Crew Application'
    CREW_PROBLEM = 'Crew Problem'
    CREW_SUBMISSION = 'Crew Submission'
    PROBLEM_REF = 'Problem Reference'
    USER = 'User'
