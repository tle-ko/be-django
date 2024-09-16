from __future__ import annotations

from django.db.models import Manager
from django.db.models import QuerySet
from django.utils import timezone

from apps.crews.db import CrewDAO
from apps.analyses.enums import ProblemDifficulty
from apps.analyses.models import ProblemAnalysis
from users.models import User

from . import db
from . import dto


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


class CrewActivity(db.CrewActivityDAO):
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


class CrewActivityProblemManager(Manager):
    def filter(self,
               crew: CrewDAO = None,
               activity: db.CrewActivityDAO = None,
               *args,
               **kwargs) -> QuerySet[CrewActivityProblem]:
        if crew is not None:
            assert isinstance(crew, CrewDAO)
            kwargs[CrewActivityProblem.field_name.CREW] = crew
        if activity is not None:
            assert isinstance(activity, db.CrewActivityDAO)
            kwargs[CrewActivityProblem.field_name.ACTIVITY] = activity
        return super().filter(*args, **kwargs)


class CrewActivityProblem(db.CrewActivityProblemDAO):
    objects: CrewActivityProblemManager = CrewActivityProblemManager()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.CrewActivityProblemDTO:
        try:
            analysis = ProblemAnalysis.objects.filter(
                problem=self.problem).first()
        except ProblemAnalysis.DoesNotExist:
            difficulty = ProblemDifficulty.UNDER_ANALYSIS
        else:
            difficulty = analysis.difficulty
        finally:
            return dto.CrewActivityProblemDTO(
                problem_id=self.pk,
                problem_ref_id=self.problem.pk,
                order=self.order,
                title=self.problem.title,
                difficulty=difficulty,
            )

    def as_submission_dto(self, user: User) -> dto.CrewActivityProblemSubmissionDTO:
        try:
            submission = CrewActivitySubmission.objects.filter(**{
                CrewActivitySubmission.field_name.PROBLEM: self,
                CrewActivitySubmission.field_name.USER: user,
            }).latest()
        except CrewActivitySubmission.DoesNotExist:
            is_submitted = False
            is_correct = False
            date_submitted_at = None
        else:
            is_submitted = True
            is_correct = submission.is_correct
            date_submitted_at = submission.created_at
        finally:
            return dto.CrewActivityProblemSubmissionDTO(
                **self.as_dto().__dict__,
                submission_id=submission.pk,
                is_submitted=is_submitted,
                is_correct=is_correct,
                date_submitted_at=date_submitted_at,
            )


class CrewActivitySubmission(db.CrewActivitySubmissionDAO):
    class Meta:
        proxy = True
