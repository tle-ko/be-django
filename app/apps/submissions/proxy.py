from __future__ import annotations

from typing import Union

from django.db.models import Manager
from django.db.models import QuerySet

from apps.activities.models import CrewActivityProblemDAO
from users.models import User

from . import models
from . import dto


class SubmissionQuerySet(QuerySet):
    def filter(self,
               problem: CrewActivityProblemDAO = None,
               submitted_by: User = None,
               **kwargs) -> Union[SubmissionQuerySet, QuerySet[Submission]]:
        return self._kwargs_filtering(
            super().filter,
            problem=problem,
            submitted_by=submitted_by,
            **kwargs,
        )

    def problem(self, problem: CrewActivityProblemDAO) -> Union[SubmissionQuerySet, QuerySet[Submission]]:
        return self.filter(problem=problem)

    def submitted_by(self, submitted_by: User) -> Union[SubmissionQuerySet, QuerySet[Submission]]:
        return self.filter(submitted_by=submitted_by)

    def _kwargs_filtering(self,
                          filter_function,
                          problem: CrewActivityProblemDAO = None,
                          submitted_by: User = None,
                          **kwargs) -> SubmissionQuerySet:
        if problem is not None:
            assert isinstance(problem, CrewActivityProblemDAO)
            kwargs[Submission.field_name.PROBLEM] = problem
        if submitted_by is not None:
            assert isinstance(submitted_by, User)
            kwargs[Submission.field_name.USER] = submitted_by
        return filter_function(**kwargs)


class Submission(models.SubmissionDAO):
    objects: SubmissionQuerySet = Manager.from_queryset(SubmissionQuerySet)()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.SubmissionDTO:
        return dto.SubmissionDTO(
            submission_id=self.pk,
            is_correct=self.is_correct,
            submitted_at=self.created_at,
            submitted_by=self.user.as_dto(),
        )


class SubmissionComment(models.SubmissionCommentDAO):
    class Meta:
        proxy = True
