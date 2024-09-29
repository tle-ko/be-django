import typing

from apps.submissions.models import SubmissionDAO
from apps.submissions.converters import SubmissionConverter
from apps.problems.converters import ProblemConverter
from apps.problems.converters import ProblemDetailConverter
from common.converters import ModelConverter
from users.models import User

from . import dto
from . import models


class CrewActivityConverter(ModelConverter[models.CrewActivityDAO, dto.CrewActivityDTO]):
    def instance_to_dto(self, instance: models.CrewActivityDAO) -> dto.CrewActivityDTO:
        return dto.CrewActivityDTO(
            activity_id=instance.pk,
            name=instance.name,
            start_at=instance.start_at,
            end_at=instance.end_at,
            is_in_progress=instance.is_in_progress(),
            has_started=instance.has_started(),
            has_ended=instance.has_ended(),
        )


class CrewActivityDetailConverter(ModelConverter[models.CrewActivityDAO, dto.CrewActivityDetailDTO]):
    def __init__(self, user: User) -> None:
        self.user = user

    def instance_to_dto(self, instance: models.CrewActivityDAO) -> dto.CrewActivityDetailDTO:
        return dto.CrewActivityDetailDTO(
            **CrewActivityConverter().instance_to_dto(instance).__dict__,
            problems=self._problems(instance),
        )

    def _problems(self, instance: models.CrewActivityDAO) -> typing.List[dto.CrewActivityProblemDTO]:
        queryset = models.CrewActivityProblemDAO.objects.filter(**{
            models.CrewActivityProblemDAO.field_name.ACTIVITY: instance,
        })
        return CrewActivityProblemConverter(self.user).queryset_to_dto(queryset)


class CrewActivityProblemSubmissionMixin:
    def _submissions(self, instance: models.CrewActivityProblemDAO) -> typing.List[dto.SubmissionDTO]:
        queryset = SubmissionDAO.objects.filter(**{
            SubmissionDAO.field_name.PROBLEM: instance,
        })
        return SubmissionConverter().queryset_to_dto(queryset)

    def _submission_id(self, instance: models.CrewActivityProblemDAO) -> typing.Optional[int]:
        try:
            return SubmissionDAO.objects.filter(**{
                SubmissionDAO.field_name.USER: self.user,
                SubmissionDAO.field_name.PROBLEM: instance,
            }).latest().pk
        except SubmissionDAO.DoesNotExist:
            return None

    def _has_submitted(self, instance: models.CrewActivityProblemDAO) -> bool:
        return self._submission_id(instance) is not None


class CrewActivityProblemConverter(ModelConverter[models.CrewActivityProblemDAO, dto.CrewActivityProblemDTO], CrewActivityProblemSubmissionMixin):
    def __init__(self, user: User) -> None:
        self.user = user

    def instance_to_dto(self, instance: models.CrewActivityProblemDAO) -> dto.CrewActivityProblemDTO:
        return dto.CrewActivityProblemDTO(
            **ProblemConverter().instance_to_dto(instance.problem).__dict__,
            problem_id=instance.pk,
            order=instance.order,
            submissions=self._submissions(instance),
            submission_id=self._submission_id(instance),
            has_submitted=self._has_submitted(instance),
        )


class CrewActivityProblemDetailConverter(ModelConverter[models.CrewActivityProblemDAO, dto.CrewActivityProblemDetailDTO], CrewActivityProblemSubmissionMixin):
    def __init__(self, user: User) -> None:
        self.user = user

    def instance_to_dto(self, instance: models.CrewActivityProblemDAO) -> dto.CrewActivityProblemDetailDTO:
        return dto.CrewActivityProblemDetailDTO(
            **ProblemDetailConverter().instance_to_dto(instance.problem).__dict__,
            problem_id=instance.pk,
            order=instance.order,
            submission_id=self._submission_id(instance),
            has_submitted=self._has_submitted(instance),
        )
