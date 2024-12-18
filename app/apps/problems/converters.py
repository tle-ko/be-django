import typing

from apps.boj.converters import BOJTagConverter
from apps.boj.models import BOJTagDAO
from common import converters

from . import enums
from . import dto
from . import models


class ProblemConverter(converters.ModelConverter[models.ProblemDAO, dto.ProblemDTO]):
    def instance_to_dto(self, instance: models.ProblemDAO) -> dto.ProblemDTO:
        return dto.ProblemDTO(
            problem_ref_id=instance.pk,
            title=instance.title,
            analysis=self._analysis(instance),
        )

    def _analysis(self, instance: models.ProblemDAO) -> dto.ProblemAnalysisDTO:
        return ProblemAnalysisConverter().problem_to_dto(instance)


class ProblemDetailConverter(ProblemConverter, converters.ModelConverter[models.ProblemDAO, dto.ProblemDetailDTO]):
    def instance_to_dto(self, instance: models.ProblemDAO) -> dto.ProblemDetailDTO:
        return dto.ProblemDetailDTO(
            problem_ref_id=instance.pk,
            title=instance.title,
            analysis=self._analysis(instance),
            link=instance.link,
            description=instance.description,
            input_description=instance.input_description,
            output_description=instance.output_description,
            memory_limit=self._memory_limit(instance),
            time_limit=self._time_limit(instance),
            created_at=instance.created_at,
        )

    def _analysis(self, instance: models.ProblemDAO) -> dto.ProblemAnalysisDTO:
        return ProblemAnalysisConverter().problem_to_dto(instance)

    def _memory_limit(self, instance: models.ProblemDAO) -> dto.ProblemLimitDTO:
        return dto.ProblemLimitDTO(
            value=instance.memory_limit,
            unit=dto.UnitDTO(enums.Unit.MEGA_BYTE),
        )

    def _time_limit(self, instance: models.ProblemDAO) -> dto.ProblemLimitDTO:
        return dto.ProblemLimitDTO(
            value=instance.time_limit,
            unit=dto.UnitDTO(enums.Unit.SECOND),
        )


class ProblemAnalysisConverter(converters.ModelConverter[models.ProblemAnalysisDAO, dto.ProblemAnalysisDTO]):
    def instance_to_dto(self, instance: models.ProblemAnalysisDAO) -> dto.ProblemAnalysisDTO:
        return dto.ProblemAnalysisDTO(
            problem_ref_id=instance.problem.pk,
            time_complexity=instance.time_complexity,
            hints=self._hints(instance),
            difficulty=self._difficulty(instance),
            tags=self._tags(instance),
            is_analyzed=self._is_analyzed(instance),
        )

    def problem_to_dto(self, problem: models.ProblemDAO) -> dto.ProblemAnalysisDTO:
        return self.instance_to_dto(self._get_instance(problem))

    def _get_instance(self, problem: models.ProblemDAO) -> models.ProblemAnalysisDAO:
        fields = {models.ProblemAnalysisDAO.field_name.PROBLEM: problem}
        try:
            return models.ProblemAnalysisDAO.objects.filter(**fields).latest()
        except models.ProblemAnalysisDAO.DoesNotExist:
            return models.ProblemAnalysisDAO.objects.create(**fields)

    def _is_analyzed(self, instance: models.ProblemAnalysisDAO) -> bool:
        return (instance.difficulty != enums.ProblemDifficulty.UNDER_ANALYSIS)

    def _difficulty(self, instance: models.ProblemAnalysisDAO) -> dto.ProblemDifficultyDTO:
        return ProblemDifficultyConverter().value_to_dto(instance.difficulty)

    def _tags(self, instance: models.ProblemAnalysisDAO) -> typing.List[dto.BOJTagDTO]:
        queryset = models.ProblemAnalysisTagDAO.objects.filter(**{
            models.ProblemAnalysisTagDAO.field_name.ANALYSIS: instance,
        })
        return ProblemTagConverter().queryset_to_dto(queryset)

    def _hints(self, instance: models.ProblemAnalysisDAO) -> typing.List[str]:
        if isinstance(instance.hints, list):
            return instance.hints
        else:
            return [instance.hints]


class ProblemDifficultyConverter(converters.ModelConverter[models.ProblemAnalysisDAO, dto.ProblemDifficultyDTO]):
    def instance_to_dto(self, instance: enums.ProblemDifficulty) -> dto.ProblemDifficultyDTO:
        return dto.ProblemDifficultyDTO(
            value=instance.value,
            name_ko=instance.get_name(lang='ko'),
            name_en=instance.get_name(lang='en'),
        )

    def value_to_dto(self, value: int) -> dto.ProblemDifficultyDTO:
        return self.instance_to_dto(enums.ProblemDifficulty(value))


class ProblemTagConverter(converters.ModelConverter[models.ProblemAnalysisTagDAO, dto.BOJTagDTO]):
    def instance_to_dto(self, instance: models.ProblemAnalysisTagDAO) -> dto.BOJTagDTO:
        return dto.BOJTagDTO(
            key=instance.tag.key,
            name_ko=instance.tag.name_ko,
            name_en=instance.tag.name_en,
        )

    def key_to_dto(self, key: str) -> dto.BOJTagDTO:
        instance = models.ProblemAnalysisTagDAO.objects.get(**{
            models.ProblemAnalysisTagDAO.field_name.TAG+"__"+BOJTagDAO.field_name.KEY: key,
        })
        return self.instance_to_dto(instance)


class ProblemStatisticConverter:
    def problem_ref_ids_to_dto(self, problem_ref_ids: typing.List[int]) -> dto.ProblemStatisticDTO:
        if not problem_ref_ids:
            return dto.ProblemStatisticDTO(problem_count=0, difficulties=[], tags=[])
        else:
            return dto.ProblemStatisticDTO(
                problem_count=len(problem_ref_ids),
                difficulties=self._difficulties(problem_ref_ids),
                tags=self._tags(problem_ref_ids),
            )

    def _difficulties(self, problem_ref_ids: typing.List[int]) -> typing.List[dto.ProblemDifficultyStaticDTO]:
        TARGET_FIELD = models.ProblemAnalysisDAO.field_name.DIFFICULTY
        COUNT_FIELD = 'count'
        queryset = models.ProblemAnalysisDAO.objects \
            .filter(**{models.ProblemAnalysisDAO.field_name.PROBLEM+"__in": problem_ref_ids}) \
            .values(TARGET_FIELD) \
            .annotate(**{COUNT_FIELD: models.models.Count(TARGET_FIELD)}) \
            .order_by(COUNT_FIELD)
        return [
            dto.ProblemDifficultyStaticDTO(
                difficulty=row[TARGET_FIELD],
                count=row[COUNT_FIELD],
                ratio=row[COUNT_FIELD]/len(problem_ref_ids),
            )
            for row in queryset
        ]

    def _tags(self, problem_ref_ids: typing.List[int]) -> typing.List[dto.ProblemTagStaticDTO]:
        TARGET_FIELD = models.ProblemAnalysisTagDAO.field_name.TAG
        COUNT_FIELD = 'count'
        queryset = models.ProblemAnalysisTagDAO.objects \
            .filter(**{models.ProblemAnalysisTagDAO.field_name.ANALYSIS+"__"+models.ProblemAnalysisDAO.field_name.PROBLEM+"__in": problem_ref_ids}) \
            .values(TARGET_FIELD) \
            .annotate(**{COUNT_FIELD: models.models.Count(TARGET_FIELD)}) \
            .order_by(COUNT_FIELD)
        return [
            dto.ProblemTagStaticDTO(
                tag=BOJTagConverter().instance_to_dto(BOJTagDAO.objects.get(pk=row[TARGET_FIELD])),
                count=row[COUNT_FIELD],
                ratio=row[COUNT_FIELD]/len(problem_ref_ids),
            )
            for row in queryset
        ]
