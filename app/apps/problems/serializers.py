from dataclasses import asdict

from rest_framework import serializers

from apps.analyses.serializers import ProblemAnalysisDTOSerializer
from apps.analyses.serializers import ProblemTagDTOSerializer

from . import models
from .models import proxy


PK = 'id'


class ProblemDTOSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField(source='pk')
    title = serializers.CharField()
    analysis = ProblemAnalysisDTOSerializer()


class ProblemDetailDTOSerializer(ProblemDTOSerializer):
    link = serializers.URLField()
    description = serializers.CharField()
    input_description = serializers.CharField()
    output_description = serializers.CharField()
    memory_limit = serializers.FloatField()
    time_limit = serializers.FloatField()
    created_at = serializers.DateTimeField()


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


class ProblemDAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProblemDAO
        fields = [
            models.ProblemDAO.field_name.TITLE,
            models.ProblemDAO.field_name.LINK,
            models.ProblemDAO.field_name.DESCRIPTION,
            models.ProblemDAO.field_name.INPUT_DESCRIPTION,
            models.ProblemDAO.field_name.OUTPUT_DESCRIPTION,
            models.ProblemDAO.field_name.MEMORY_LIMIT,
            models.ProblemDAO.field_name.TIME_LIMIT,
            models.ProblemDAO.field_name.CREATED_BY,
        ]
        read_only_fields = [
            models.ProblemDAO.field_name.CREATED_BY,
        ]
        extra_kwargs = {
            models.ProblemDAO.field_name.CREATED_BY: {
                'default': serializers.CurrentUserDefault(),
            },
        }

    @property
    def data(self):
        self.instance: models.ProblemDAO
        obj = proxy.Problem.objects.get(pk=self.instance.pk)
        return asdict(obj.as_detail_dto())


class ProblemSearchQueryParamSerializer(serializers.Serializer):
    q = serializers.CharField(required=False, default=None)


# class AnalysisSerializer(ProblemAnalysisSerializer):
#     def to_representation(self, analysis: Optional[ProblemAnalysis]):
#         if analysis is None:
#             return {
#                 'is_analyzed': False,
#             }
#         else:
#             return {
#                 'is_analyzed': True,
#                 **super().to_representation(analysis),
#             }

#     def get_attribute(self, instance: Problem) -> Optional[ProblemAnalysis]:
#         assert isinstance(instance, Problem)
#         try:
#             return ProblemAnalysis.objects.get_by_problem(instance)
#         except ProblemAnalysis.DoesNotExist:
#             return None


# class ProblemLimitsField(serializers.SerializerMethodField):
#     def to_representation(self, problem: models.Problem):
#         assert isinstance(problem, models.Problem)
#         return {
#             "memory": {
#                 "value": problem.memory_limit,
#                 "unit": UnitSerializer(Unit(problem.memory_limit_unit)).data,
#             },
#             "time_limit": {
#                 "value": problem.time_limit,
#                 "unit": UnitSerializer(Unit(problem.time_limit_unit)).data,
#             },
#         }


# class ProblemDifficultyField(ProblemAnalysisDifficultyField):
#     def get_attribute(self, instance: Problem) -> ProblemDifficulty:
#         try:
#             analysis = ProblemAnalysis.objects.get_by_problem(instance)
#         except ProblemAnalysis.DoesNotExist:
#             return ProblemDifficulty.UNDER_ANALYSIS
#         else:
#             return ProblemDifficulty(analysis.difficulty)


# class ProblemDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ProblemDAO
#         fields = [
#             models.ProblemDAO.field_name.TITLE,
#             models.ProblemDAO.field_name.LINK,
#             models.ProblemDAO.field_name.DESCRIPTION,
#             models.ProblemDAO.field_name.INPUT_DESCRIPTION,
#             models.ProblemDAO.field_name.OUTPUT_DESCRIPTION,
#             models.ProblemDAO.field_name.MEMORY_LIMIT,
#             models.ProblemDAO.field_name.TIME_LIMIT,
#             models.ProblemDAO.field_name.CREATED_BY,
#             models.ProblemDAO.field_name.UPDATED_AT,
#         ]
#         read_only_fields = [
#             models.ProblemDAO.field_name.CREATED_BY,
#             models.ProblemDAO.field_name.UPDATED_AT,
#         ]

#     @property
#     def data(self):
#         obj = models.Problem.objects.get(self.instance.pk)
#         return asdict(obj.as_detail_dto())


# class ProblemMinimalSerializer(serializers.ModelSerializer):
#     difficulty = ProblemDifficultyField()

#     class Meta:
#         model = models.Problem
#         fields = [
#             'id',
#             models.Problem.field_name.TITLE,
#             'difficulty',
#             models.Problem.field_name.CREATED_AT,
#             models.Problem.field_name.UPDATED_AT,
#         ]
#         read_only_fields = ['__all__']


# class UnitSerializer(serializers.Serializer):
#     def to_representation(self, unit: Unit):
#         assert isinstance(unit, Unit)
#         return {
#             'name': unit.label,
#             'value': unit.value,
#         }
