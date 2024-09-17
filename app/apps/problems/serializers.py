from typing import Optional

from rest_framework import serializers

from apps.problems import dto
from apps.problems import models
from apps.analyses.enums import ProblemDifficulty
from apps.analyses.models import ProblemAnalysis
from apps.analyses.serializers import ProblemAnalysisSerializer
from apps.analyses.serializers import ProblemAnalysisDifficultyField
from apps.analyses.serializers import ProblemTagDTOSerializer
from apps.problems.dto import ProblemStatisticDTO
from apps.problems.enums import Unit
from apps.problems.models import Problem
from users.serializers import UserMinimalSerializer


PK = 'id'


class ProblemDifficultyStatisticDTOSerializer(serializers.Serializer):
    difficulty = serializers.IntegerField()
    count = serializers.IntegerField()
    ratio = serializers.FloatField()


class ProblemTagStaticDTOSerializer(serializers.Serializer):
    tag = ProblemTagDTOSerializer()
    count = serializers.IntegerField()
    ratio = serializers.FloatField()


class ProblemStatisticDTOSerializer(serializers.Serializer):
    problem_count = serializers.IntegerField()
    difficulties = ProblemDifficultyStatisticDTOSerializer(many=True)
    tags = ProblemTagStaticDTOSerializer(many=True)


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


class UnitSerializer(serializers.Serializer):
    def to_representation(self, unit: Unit):
        assert isinstance(unit, Unit)
        return {
            'name': unit.label,
            'value': unit.value,
        }
