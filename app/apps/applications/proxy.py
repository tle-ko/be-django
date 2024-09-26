from __future__ import annotations

from typing import Union

from django.db.models import Manager
from django.db.models import QuerySet
from django.db.transaction import atomic
from django.dispatch import receiver
from django.utils import timezone

from apps.crews.models import CrewDAO
from apps.crews.models import CrewMemberDAO
from users.models import User

from . import dto
from . import mail
from . import models
from . import signals


class CrewApplicationQuerySet(QuerySet):
    def create(self,
               crew: CrewDAO,
               applicant: User,
               message: str,
               *args,
               **kwargs) -> CrewApplication:
        kwargs[CrewApplication.field_name.CREW] = crew
        kwargs[CrewApplication.field_name.APPLICANT] = applicant
        kwargs[CrewApplication.field_name.MESSAGE] = message
        return super().create(**kwargs)

    def exclude(self,
                crew: CrewDAO = None,
                applicant: User = None,
                *args,
                **kwargs) -> Union[CrewApplicationQuerySet, QuerySet[CrewApplication]]:
        return self._kwargs_filtering(super().exclude, crew, applicant, *args, **kwargs)

    def filter(self,
               crew: CrewDAO = None,
               applicant: User = None,
               *args,
               **kwargs) -> Union[CrewApplicationQuerySet, QuerySet[CrewApplication]]:
        return self._kwargs_filtering(super().filter, crew, applicant, *args, **kwargs)

    def crew(self, crew: CrewDAO) -> Union[CrewApplicationQuerySet, QuerySet[CrewApplication]]:
        return self.filter(crew=crew)

    def applicant(self, applicant: User) -> Union[CrewApplicationQuerySet, QuerySet[CrewApplication]]:
        return self.filter(applicant=applicant)

    def _kwargs_filtering(self,
                          filter_function,
                          crew: CrewDAO = None,
                          applicant: User = None,
                          **kwargs) -> CrewApplicationQuerySet:
        if crew is not None:
            isinstance(crew, CrewDAO)
            kwargs[CrewApplication.field_name.CREW] = crew
        if applicant is not None:
            isinstance(applicant, User)
            kwargs[CrewApplication.field_name.APPLICANT] = applicant
        return filter_function(**kwargs)


class CrewApplication(models.CrewApplicationDAO):
    objects: Union[CrewApplicationQuerySet, QuerySet[CrewApplication]]
    objects = Manager.from_queryset(CrewApplicationQuerySet)()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.CrewApplicationDTO:
        return dto.CrewApplicationDTO(
            application_id=self.pk,
            applicant=dto.CrewApplicantDTO.from_user(self.applicant),
            message=self.message,
            is_pending=self.is_pending,
            is_accepted=self.is_accepted,
            created_at=self.created_at,
        )

    def create_member(self) -> CrewMemberDAO:
        return CrewMemberDAO.objects.create(**{
            CrewMemberDAO.field_name.CREW: self.crew,
            CrewMemberDAO.field_name.USER: self.applicant,
            CrewMemberDAO.field_name.IS_CAPTAIN: False,
        })

    def accept(self, reviewed_by: User):
        self.review(reviewed_by, is_accepted=True)

    def reject(self, reviewed_by: User):
        self.review(reviewed_by, is_accepted=False)

    def review(self, reviewed_by: User, is_accepted: bool):
        self.is_pending = False
        self.is_accepted = is_accepted
        self.reviewed_by = reviewed_by
        self.reviewed_at = timezone.now()
        with atomic():
            self.save()
            if self.is_accepted:
                self.create_member()
                signals.accepted.send(sender=CrewApplication, instance=self)
            else:
                signals.rejected.send(sender=CrewApplication, instance=self)
        signals.reviewed.send(sender=CrewApplication, instance=self)


@receiver(signals.post_save, sender=CrewApplication)
def notify_on_applied(sender, instance: CrewApplication, created: bool, **kwargs):
    if created:
        mail.notify_application_recieved(instance)


@receiver(signals.accepted, sender=CrewApplication)
def notify_on_accepted(sender, instance: CrewApplication, **kwargs):
    mail.notify_application_accepted(instance)


@receiver(signals.rejected, sender=CrewApplication)
def notify_on_rejected(sender, instance: CrewApplication, **kwargs):
    mail.notify_application_rejected(instance)
