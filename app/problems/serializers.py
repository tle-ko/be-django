from typing import Optional

from rest_framework import serializers

from problems import dto
from problems import models
from problems.analyses.enums import ProblemDifficulty
from problems.analyses.models import ProblemAnalysis
from problems.analyses.serializers import ProblemAnalysisSerializer
from problems.analyses.serializers import ProblemAnalysisDifficultyField
from problems.dto import ProblemStatisticDTO
from problems.enums import Unit
from problems.models import Problem
from users.serializers import UserMinimalSerializer


PK = 'id'


class AnalysisSerializer(ProblemAnalysisSerializer):
    def to_representation(self, analysis: Optional[ProblemAnalysis]):
        if analysis is None:
            return {
                'is_analyzed': False,
            }
        else:
            return {
                'is_analyzed': True,
                **super().to_representation(analysis),
            }

    def get_attribute(self, instance: Problem) -> Optional[ProblemAnalysis]:
        assert isinstance(instance, Problem)
        try:
            return ProblemAnalysis.objects.get_by_problem(instance)
        except ProblemAnalysis.DoesNotExist:
            return None


class ProblemLimitsField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        return {
            "memory": {
                "value": problem.memory_limit,
                "unit": UnitSerializer(Unit(problem.memory_limit_unit)).data,
            },
            "time_limit": {
                "value": problem.time_limit,
                "unit": UnitSerializer(Unit(problem.time_limit_unit)).data,
            },
        }


class ProblemDifficultyField(ProblemAnalysisDifficultyField):
    def get_attribute(self, instance: Problem) -> ProblemDifficulty:
        try:
            analysis = ProblemAnalysis.objects.get_by_problem(instance)
        except ProblemAnalysis.DoesNotExist:
            return ProblemDifficulty.UNDER_ANALYSIS
        else:
            return ProblemDifficulty(analysis.difficulty)


class ProblemStatisticsDifficultyField(serializers.SerializerMethodField):
    def to_representation(self, statistics: dto.ProblemStatisticDTO):
        assert isinstance(statistics, dto.ProblemStatisticDTO)
        try:
            ratio_denominator = 1 / statistics.sample_count
        except ZeroDivisionError:
            ratio_denominator = 0
        finally:
            return [
                {
                    'difficulty': difficulty,
                    'problem_count': count,
                    'ratio': count * ratio_denominator,
                }
                for difficulty, count in statistics.difficulty.items()
            ]


class ProblemStatisticsTagsField(serializers.SerializerMethodField):
    def to_representation(self, statistics: dto.ProblemStatisticDTO):
        assert isinstance(statistics, dto.ProblemStatisticDTO)
        try:
            ratio_denominator = 1 / statistics.sample_count
        except ZeroDivisionError:
            ratio_denominator = 0
        finally:
            return [
                {
                    'label': {
                        'ko': tag.name_ko,
                        'en': tag.name_en,
                    },
                    'problem_count': count,
                    'ratio': count * ratio_denominator,
                }
                for tag, count in statistics.tags.items()
            ]


class ProblemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = [
            models.Problem.field_name.TITLE,
            models.Problem.field_name.LINK,
            models.Problem.field_name.DESCRIPTION,
            models.Problem.field_name.INPUT_DESCRIPTION,
            models.Problem.field_name.OUTPUT_DESCRIPTION,
            models.Problem.field_name.MEMORY_LIMIT,
            models.Problem.field_name.TIME_LIMIT,
        ]


class ProblemDetailSerializer(serializers.ModelSerializer):
    analysis = AnalysisSerializer()
    limits = ProblemLimitsField()
    created_by = UserMinimalSerializer()

    class Meta:
        model = models.Problem
        fields = [
            PK,
            models.Problem.field_name.TITLE,
            models.Problem.field_name.LINK,
            'limits',
            models.Problem.field_name.DESCRIPTION,
            models.Problem.field_name.INPUT_DESCRIPTION,
            models.Problem.field_name.OUTPUT_DESCRIPTION,
            models.Problem.field_name.MEMORY_LIMIT,
            models.Problem.field_name.TIME_LIMIT,
            models.Problem.field_name.CREATED_AT,
            models.Problem.field_name.UPDATED_AT,
            'created_by',
            'analysis',
        ]
        extra_kwargs = {
            PK: {'read_only': True},
            models.Problem.field_name.MEMORY_LIMIT: {'write_only': True},
            models.Problem.field_name.TIME_LIMIT: {'write_only': True},
            models.Problem.field_name.CREATED_AT: {'read_only': True},
            models.Problem.field_name.UPDATED_AT: {'read_only': True},
            'created_by': {
                'read_only': True,
                'default': serializers.CurrentUserDefault(),
            }
        }


class ProblemMinimalSerializer(serializers.ModelSerializer):
    difficulty = ProblemDifficultyField()

    class Meta:
        model = models.Problem
        fields = [
            'id',
            models.Problem.field_name.TITLE,
            'difficulty',
            models.Problem.field_name.CREATED_AT,
            models.Problem.field_name.UPDATED_AT,
        ]
        read_only_fields = ['__all__']


class ProblemStatisticSerializer(serializers.Serializer):
    difficulty = ProblemStatisticsDifficultyField()
    tags = ProblemStatisticsTagsField()

    def __init__(self, instance: ProblemStatisticDTO = None, **kwargs):
        super().__init__(instance, **kwargs)


class UnitSerializer(serializers.Serializer):
    def to_representation(self, unit: Unit):
        assert isinstance(unit, Unit)
        return {
            'name': unit.label,
            'value': unit.value,
        }
