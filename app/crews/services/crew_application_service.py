from django.db.transaction import atomic
from django.utils import timezone

import notifications.services
import users.models
from crews import models


class CrewApplicantionService:
    @staticmethod
    def create(crew: models.Crew, user: users.models.User, message: str) -> models.CrewApplicant:
        instance = models.CrewApplicant(**{
            models.CrewApplicant.field_name.CREW: crew,
            models.CrewApplicant.field_name.USER: user,
            models.CrewApplicant.field_name.MESSAGE: message,
        })
        instance.save()
        notifications.services.notify_crew_application_requested(instance)

    def __init__(self, instance: models.CrewApplicant):
        assert isinstance(instance, models.CrewApplicant)
        self.instance = instance

    def reject(self, reviewed_by: users.models.User):
        self.instance.is_accepted = False
        self.instance.reviewed_by = reviewed_by
        self.instance.reviewed_at = timezone.now()
        self.instance.save()
        notifications.services.notify_crew_application_rejected(self.instance)

    def accept(self, reviewed_by: users.models.User):
        self.instance.is_accepted = True
        self.instance.reviewed_by = reviewed_by
        self.instance.reviewed_at = timezone.now()
        with atomic():
            self.instance.save()
            models.CrewMember.objects.create(**{
                models.CrewApplicant.field_name.CREW: self.instance.crew,
                models.CrewApplicant.field_name.USER: self.instance.user,
            })
        notifications.services.notify_crew_application_accepted(self.instance)
