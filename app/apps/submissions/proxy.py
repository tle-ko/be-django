from __future__ import annotations

import typing

from django.db.models import Manager
from django.db.models import QuerySet

from apps.crews.models import CrewProblemDAO
from users.dto import UserDTO
from users.models import User

from . import models
from . import dto


class SubmissionQuerySet(QuerySet):
    def filter(self,
               problem: CrewProblemDAO = None,
               submitted_by: User = None,
               **kwargs) -> typing.Union[SubmissionQuerySet, QuerySet[Submission]]:
        return self._kwargs_filtering(
            super().filter,
            problem=problem,
            submitted_by=submitted_by,
            **kwargs,
        )

    def problem(self, problem: CrewProblemDAO) -> typing.Union[SubmissionQuerySet, QuerySet[Submission]]:
        return self.filter(problem=problem)

    def submitted_by(self, submitted_by: User) -> typing.Union[SubmissionQuerySet, QuerySet[Submission]]:
        return self.filter(submitted_by=submitted_by)

    def _kwargs_filtering(self,
                          filter_function,
                          problem: CrewProblemDAO = None,
                          submitted_by: User = None,
                          **kwargs) -> SubmissionQuerySet:
        if problem is not None:
            assert isinstance(problem, CrewProblemDAO)
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
            reviewers=self.reviewers(),
        )

    def as_detail_dto(self) -> dto.SubmissionDetailDTO:
        return dto.SubmissionDetailDTO(
            **self.as_dto().__dict__,
            code=self.code,
            comments=[obj.as_dto() for obj in self.comments()],
        )

    def get_user_dto(self) -> UserDTO:
        return self.user.as_dto()

    def comments(self) -> QuerySet[SubmissionComment]:
        return SubmissionComment.objects.filter(submission=self)

    def reviewers(self) -> typing.List[UserDTO]:
        reviewer_id_list = models.SubmissionCommentDAO.objects \
            .filter(**{models.SubmissionCommentDAO.field_name.SUBMISSION: self}) \
            .values_list(models.SubmissionCommentDAO.field_name.CREATED_BY, flat=True) \
            .distinct()
        return [obj.as_dto() for obj in User.objects.filter(pk__in=reviewer_id_list)]


class SubmissionComment(models.SubmissionCommentDAO):
    class Meta:
        proxy = True

    def as_dto(self) -> dto.SubmissionCommentDTO:
        return dto.SubmissionCommentDTO(
            comment_id=self.pk,
            content=self.content,
            line_number_start=self.line_number_start,
            line_number_end=self.line_number_end,
            created_at=self.created_at,
            created_by=self.created_by.as_dto(),
        )
