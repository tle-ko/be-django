from crews.servicesa.base import UserCrewService
from crews.servicesa.base import CrewService
from crews.servicesa.base import CrewActivityService
from crews.servicesa.base import CrewApplicantionService
from crews.servicesa.concrete import ConcreteUserCrewService
from crews.servicesa.concrete import ConcreteCrewService

from crews import models
from users.models import User


def get_user_crew_service(user: User) -> UserCrewService:
    return ConcreteUserCrewService(user)


def get_crew_service(crew: models.Crew) -> CrewService:
    return ConcreteCrewService(crew)


def get_crew_activity_service(crew_activity: models.CrewActivity) -> CrewActivityService:
    return CrewActivityService(crew_activity)


def get_crew_application_service(crew_application: models.CrewApplication) -> CrewApplicantionService:
    return CrewApplicantionService(crew_application)
