from django.db.transaction import atomic
from django.utils import timezone

import notifications.services
import users.models
from crews import models


class CrewApplicantionService:
    @staticmethod
    def create(crew: models.Crew, user: users.models.User, message: str) -> models.CrewApplication:
        instance = models.CrewApplication(**{
            models.CrewApplication.field_name.CREW: crew,
            models.CrewApplication.field_name.APPLICANT: user,
            models.CrewApplication.field_name.MESSAGE: message,
        })
        instance.save()
        notifications.services.notify_crew_application_requested(instance)

    def __init__(self, instance: models.CrewApplication):
        assert isinstance(instance, models.CrewApplication)
        self.instance = instance

    def reject(self, reviewed_by: users.models.User):
        self._review(reviewed_by, accept=False)
        self.instance.save()
        notifications.services.notify_crew_application_rejected(self.instance)

    def accept(self, reviewed_by: users.models.User):
        self._review(reviewed_by, accept=True)
        with atomic():
            self.instance.save()
            models.CrewMember.objects.create(**{
                models.CrewApplication.field_name.CREW: self.instance.crew,
                models.CrewApplication.field_name.APPLICANT: self.instance.applicant,
            })
        notifications.services.notify_crew_application_accepted(self.instance)

    def _review(self, by: users.models.User, accept: bool):
        self.instance.is_pending = False
        self.instance.is_accepted = accept
        self.instance.reviewed_by = by
        self.instance.reviewed_at = timezone.now()
