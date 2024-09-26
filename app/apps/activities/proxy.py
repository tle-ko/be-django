from __future__ import annotations

from typing import List
from typing import Optional
from typing import Union

from django.db.models import Manager
from django.db.models import QuerySet
from django.utils import timezone

from apps.crews.models import CrewDAO
from apps.submissions.dto import SubmissionDTO
from apps.submissions.proxy import Submission
from users.models import User

from . import dto
from . import models


class CrewActivityManager(Manager):
    def filter(self,
               crew: CrewDAO = None,
               has_started: bool = None,
               in_progress: bool = None,
               *args,
               **kwargs) -> QuerySet[CrewActivity]:
        now = timezone.now()
        if crew is not None:
            assert isinstance(crew, CrewDAO)
            kwargs[CrewActivity.field_name.CREW] = crew
        if has_started is not None:
            kwargs[CrewActivity.field_name.START_AT + '__lte'] = now
        if in_progress is not None:
            kwargs[CrewActivity.field_name.START_AT + '__lte'] = now
            kwargs[CrewActivity.field_name.END_AT + '__gt'] = now
        return super().filter(*args, **kwargs)


class CrewActivity(models.CrewActivityDAO):
    objects: CrewActivityManager = CrewActivityManager()

    class Meta:
        proxy = True

    def is_in_progress(self) -> bool:
        return self.has_started() and not self.has_ended()

    def has_started(self) -> bool:
        return self.start_at <= timezone.now()

    def has_ended(self) -> bool:
        return self.end_at < timezone.now()

    def problems(self) -> QuerySet[CrewActivityProblem]:
        return CrewActivityProblem.objects.filter(activity=self)

    def problem_details(self, user: User) -> List[dto.CrewActivityDetailDTO]:
        return CrewActivityProblem.objects.filter(activity=self).as_detail_dto(user)

    def as_dto(self) -> dto.CrewActivityDTO:
        return dto.CrewActivityDTO(
            activity_id=self.pk,
            name=self.name,
            start_at=self.start_at,
            end_at=self.end_at,
            is_in_progress=self.is_in_progress(),
            has_started=self.has_started(),
            has_ended=self.has_ended(),
        )

    def as_detail_dto(self, user: User) -> dto.CrewActivityDetailDTO:
        return dto.CrewActivityDetailDTO(
            **self.as_dto().__dict__,
            problems=[obj.as_detail_dto(user) for obj in self.problems().all()],
        )


class CrewActivityQuerySet(QuerySet):
    def filter(self,
               crew: CrewDAO = None,
               activity: models.CrewActivityDAO = None,
               *args,
               **kwargs) -> Union[CrewActivityQuerySet, QuerySet[CrewActivityProblem]]:
        if crew is not None:
            assert isinstance(crew, CrewDAO)
            kwargs[CrewActivityProblem.field_name.CREW] = crew
        if activity is not None:
            assert isinstance(activity, models.CrewActivityDAO)
            kwargs[CrewActivityProblem.field_name.ACTIVITY] = activity
        return super().filter(*args, **kwargs)

    def as_detail_dto(self: QuerySet[CrewActivityProblem], user: User) -> List[dto.CrewActivityProblemDetailDTO]:
        return [obj.as_detail_dto(user) for obj in self]


class CrewActivityProblem(models.CrewActivityProblemDAO):
    objects: Union[CrewActivityQuerySet, QuerySet[CrewActivityProblem]]
    objects = Manager.from_queryset(CrewActivityQuerySet)()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.CrewActivityProblemDTO:
        obj = dto.CrewActivityProblemDTO(
            **self.problem.as_dto().__dict__,
            problem_ref_id=self.problem.pk,
            order=self.order,
        )
        obj.problem_id = self.pk
        return obj

    def as_detail_dto(self, user: User) -> dto.CrewActivityProblemDetailDTO:
        return dto.CrewActivityProblemDetailDTO(
            **self.as_dto().__dict__,
            submissions=self.submissions(),
            my_submission=self.submission_of_user(user),
        )

    def submissions(self) -> List[SubmissionDTO]:
        return [obj.as_dto() for obj in Submission.objects.problem(self)]

    def submission_of_user(self, user: User) -> Optional[SubmissionDTO]:
        try:
            obj = Submission.objects.problem(self).submitted_by(user).latest()
        except Submission.DoesNotExist:
            return None
        else:
            return obj.as_dto()
