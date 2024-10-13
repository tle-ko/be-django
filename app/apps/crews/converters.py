from __future__ import annotations

import typing

from apps.boj.converters import BOJUserConverter
from apps.boj.enums import BOJLevel
from apps.submissions.converters import SubmissionConverter
from apps.submissions.models import SubmissionDAO
from apps.problems.converters import ProblemStatisticConverter
from apps.problems.converters import ProblemConverter
from apps.problems.converters import ProblemDetailConverter
from common import converters
from users.converters import UserConverter

from . import enums
from . import dto
from . import models


class CrewConverter(converters.ModelConverter[models.CrewDAO, dto.CrewDTO]):
    def instance_to_dto(self, instance: models.CrewDAO) -> dto.CrewDTO:
        return dto.CrewDTO(
            crew_id=instance.pk,
            name=instance.name,
            icon=instance.icon,
            is_active=instance.is_active,
            is_recruiting=instance.is_recruiting,
            latest_activity=self._latest_activity(instance),
            member_count=self._member_count(instance),
            tags=self._tags(instance),
        )

    def _latest_activity(self, instance: models.CrewDAO):
        if not instance.is_active:
            return CrewActivityConverter().name_to_dto('활동 종료')
        try:
            activity = models.CrewActivityDAO.objects \
                .filter(**{models.CrewActivityDAO.field_name.CREW: instance}) \
                .latest()
            return CrewActivityConverter().instance_to_dto(activity)
        except models.CrewActivityDAO.DoesNotExist:
            return CrewActivityConverter().name_to_dto('등록된 활동 없음')

    def _member_count(self, instance: models.CrewDAO):
        return dto.CrewMemberCountDTO(
            count=models.CrewMemberDAO.objects.filter(crew=instance).count(),
            max_count=instance.max_members,
        )

    def _tags(self, instance: models.CrewDAO):
        objects = []
        for submittable_language in models.CrewSubmittableLanguageDAO.objects \
                .filter(**{models.CrewSubmittableLanguageDAO.field_name.CREW: instance}):
            obj = CrewTagConverter().submittable_language_to_dto(enums.ProgrammingLanguageChoices(submittable_language.language))
            objects.append(obj)
        if instance.min_boj_level is not None:
            obj = CrewTagConverter().boj_level_to_dto(BOJLevel(instance.min_boj_level))
            objects.append(obj)
        for custom_tag in instance.custom_tags:
            obj = CrewTagConverter().custom_to_dto(custom_tag)
            objects.append(obj)
        return objects


class CrewDetailConverter(converters.UserRequiredModelConverter[models.CrewDAO, dto.CrewDetailDTO]):
    def instance_to_dto(self, instance: models.CrewDAO) -> dto.CrewDetailDTO:
        return dto.CrewDetailDTO(
            **CrewConverter().instance_to_dto(instance).__dict__,
            notice=instance.notice,
            members=self._members(instance),
            activities=self._activities(instance),
            is_captain=self._is_captain(instance),
        )

    def _members(self, instance: models.CrewDAO):
        queryset = models.CrewMemberDAO.objects \
            .filter(**{models.CrewMemberDAO.field_name.CREW: instance})
        return CrewMemberConverter().queryset_to_dto(queryset)

    def _activities(self, instance: models.CrewDAO):
        queryset = models.CrewActivityDAO.objects \
            .filter(**{models.CrewActivityDAO.field_name.CREW: instance})
        return CrewActivityConverter().queryset_to_dto(queryset)

    def _is_captain(self, instance: models.CrewDAO):
        return models.CrewMemberDAO.objects \
            .filter(**{models.CrewMemberDAO.field_name.CREW: instance, models.CrewMemberDAO.field_name.USER: self.user}) \
            .exists()


class CrewMemberConverter(converters.ModelConverter[models.CrewMemberDAO, dto.CrewMemberDTO]):
    def instance_to_dto(self, instance: models.CrewMemberDAO) -> dto.CrewMemberDTO:
        return dto.CrewMemberDTO(
            **UserConverter().instance_to_dto(instance.user).__dict__,
            is_captain=instance.is_captain,
        )


class CrewTagConverter:
    def custom_to_dto(self, name: str) -> dto.CrewTagDTO:
        return dto.CrewTagDTO(
            key=None,
            name=name,
            type=enums.CrewTagType.CUSTOM,
        )

    def submittable_language_to_dto(self, language: enums.ProgrammingLanguageChoices) -> dto.CrewTagDTO:
        assert isinstance(language, enums.ProgrammingLanguageChoices)
        return dto.CrewTagDTO(
            key=language.value,
            name=language.label,
            type=enums.CrewTagType.LANGUAGE,
        )

    def boj_level_to_dto(self, level: BOJLevel) -> dto.CrewTagDTO:
        assert isinstance(level, BOJLevel)
        if level == BOJLevel.U:
            tag_name = '티어 무관'
        elif level.get_tier() == 5:
            tag_name = f"{level.get_division_name()} 이상"
        else:
            tag_name = f"{level.get_name()} 이상"
        return dto.CrewTagDTO(
            key=None,
            name=tag_name,
            type=enums.CrewTagType.LEVEL,
        )


class CrewApplicantConverter(converters.UserRequiredModelConverter[models.User, dto.CrewApplicantDTO]):
    def instance_to_dto(self, instance: models.User) -> dto.CrewApplicantDTO:
        return dto.CrewApplicantDTO(
            **UserConverter().instance_to_dto(instance).__dict__,
            boj=BOJUserConverter().username_to_dto(instance.boj_username),
        )


class CrewApplicationConverter(converters.UserRequiredModelConverter[models.CrewApplicationDAO, dto.CrewApplicationDTO]):
    def instance_to_dto(self, instance: models.CrewApplicationDAO) -> dto.CrewApplicationDTO:
        return dto.CrewApplicationDTO(
            application_id=instance.pk,
            applicant=CrewApplicantConverter(
                self.user).instance_to_dto(instance.applicant),
            message=instance.message,
            is_pending=instance.is_pending,
            is_accepted=instance.is_accepted,
            created_at=instance.created_at,
        )


class CrewStatisticsConverter(converters.ModelConverter[models.CrewDAO, dto.CrewStatisticsDTO]):
    def instance_to_dto(self, instance: models.CrewDAO) -> dto.CrewStatisticsDTO:
        problem_ref_ids = models.CrewProblemDAO.objects \
            .filter(**{models.CrewProblemDAO.field_name.CREW: instance}) \
            .values_list(models.CrewProblemDAO.field_name.PROBLEM, flat=True)
        return ProblemStatisticConverter().problem_ref_ids_to_dto(problem_ref_ids)


class CrewActivityConverter(converters.ModelConverter[models.CrewActivityDAO, dto.CrewActivityDTO]):
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

    def name_to_dto(self, name: str) -> dto.CrewActivityDTO:
        return dto.CrewActivityDTO(
            activity_id=None,
            name=name,
            start_at=None,
            end_at=None,
            is_in_progress=False,
            has_started=False,
            has_ended=False,
        )


class CrewActivityDetailConverter(converters.UserRequiredModelConverter[models.CrewActivityDAO, dto.CrewActivityDetailDTO]):
    def instance_to_dto(self, instance: models.CrewActivityDAO) -> dto.CrewActivityDetailDTO:
        return dto.CrewActivityDetailDTO(
            **CrewActivityConverter().instance_to_dto(instance).__dict__,
            problems=self._problems(instance),
        )

    def _problems(self, instance: models.CrewActivityDAO) -> typing.List[dto.CrewProblemDTO]:
        queryset = models.CrewProblemDAO.objects.filter(**{
            models.CrewProblemDAO.field_name.ACTIVITY: instance,
        })
        return CrewActivityProblemConverter(self.user).queryset_to_dto(queryset)


class CrewActivityProblemConverter(converters.UserRequiredModelConverter[models.CrewProblemDAO, dto.CrewProblemDTO]):
    def instance_to_dto(self, instance: models.CrewProblemDAO) -> dto.CrewProblemDTO:
        return dto.CrewProblemDTO(
            **ProblemConverter().instance_to_dto(instance.problem).__dict__,
            problem_id=instance.pk,
            order=instance.order,
            submissions=self._submissions(instance),
            submission_id=self._submission_id(instance),
            has_submitted=self._has_submitted(instance),
        )

    def _submissions(self, instance: models.CrewProblemDAO) -> typing.List[dto.SubmissionDTO]:
        queryset = SubmissionDAO.objects \
            .filter(**{SubmissionDAO.field_name.PROBLEM: instance})
        return SubmissionConverter().queryset_to_dto(queryset)

    def _submission_id(self, instance: models.CrewProblemDAO) -> typing.Optional[int]:
        try:
            return SubmissionDAO.objects \
                .filter(**{SubmissionDAO.field_name.USER: self.user, SubmissionDAO.field_name.PROBLEM: instance}) \
                .latest().pk
        except SubmissionDAO.DoesNotExist:
            return None

    def _has_submitted(self, instance: models.CrewProblemDAO) -> bool:
        return self._submission_id(instance) is not None


class CrewActivityProblemDetailConverter(converters.UserRequiredModelConverter[models.CrewProblemDAO, dto.CrewProblemDetailDTO]):
    def __init__(self, user: models.User) -> None:
        self.user = user

    def instance_to_dto(self, instance: models.CrewProblemDAO) -> dto.CrewProblemDetailDTO:
        return dto.CrewProblemDetailDTO(
            **ProblemDetailConverter().instance_to_dto(instance.problem).__dict__,
            problem_id=instance.pk,
            order=instance.order,
            submission_id=self._submission_id(instance),
            has_submitted=self._has_submitted(instance),
        )

    def _submission_id(self, instance: models.CrewProblemDAO) -> typing.Optional[int]:
        try:
            return SubmissionDAO.objects \
                .filter(**{SubmissionDAO.field_name.USER: self.user, SubmissionDAO.field_name.PROBLEM: instance}) \
                .latest().pk
        except SubmissionDAO.DoesNotExist:
            return None

    def _has_submitted(self, instance: models.CrewProblemDAO) -> bool:
        return self._submission_id(instance) is not None
