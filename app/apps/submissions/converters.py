import typing

from common.converters import ModelConverter
from users.converters import UserConverter
from users.models import User

from . import dto
from . import models


class SubmissionConverter(ModelConverter[models.SubmissionDAO, dto.SubmissionDTO]):
    def instance_to_dto(self, instance: models.SubmissionDAO) -> dto.SubmissionDTO:
        return dto.SubmissionDTO(
            submission_id=instance.pk,
            is_correct=instance.is_correct,
            submitted_at=instance.created_at,
            submitted_by=UserConverter().instance_to_dto(instance.user),
            reviewers=self._reviewers(instance),
        )

    def _reviewers(self, instance: models.SubmissionDAO) -> typing.List[dto.UserDTO]:
        reviewer_ids = models.SubmissionCommentDAO.objects.filter(**{
            models.SubmissionCommentDAO.field_name.SUBMISSION: instance,
        }).values_list(
            models.SubmissionCommentDAO.field_name.CREATED_BY,
            flat=True,
        ).distinct()
        queryset = User.objects.filter(pk__in=reviewer_ids)
        return UserConverter().queryset_to_dto(queryset)
