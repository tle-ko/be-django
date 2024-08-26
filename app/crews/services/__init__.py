from crews.services.base import UserCrewService
from crews.services.base import CrewService
from crews.services.base import CrewActivityService
from crews.services.base import CrewApplicantionService

from crews import models
from users.models import User


def get_user_crew_service(user: User) -> UserCrewService:
    return UserCrewService(user)


def get_crew_service(crew: models.Crew) -> CrewService:
    return CrewService(crew)


def get_crew_activity_service(crew_activity: models.CrewActivity) -> CrewActivityService:
    return CrewActivityService(crew_activity)


def get_crew_application_service(crew_application: models.CrewApplication) -> CrewApplicantionService:
    return CrewApplicantionService(crew_application)
