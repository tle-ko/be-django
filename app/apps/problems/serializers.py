from rest_framework import serializers

from apps.boj.serializers import BOJTagDTOSerializer
from common.serializers import GenericModelToDTOSerializer

from . import converters
from . import dto
from . import models


PK = 'id'


class ProblemDifficultyDTOSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    name_ko = serializers.CharField()
    name_en = serializers.CharField()


class ProblemAnalysisDTOSerializer(serializers.Serializer):
    problem_ref_id = serializers.IntegerField()
    time_complexity = serializers.CharField()
    difficulty = ProblemDifficultyDTOSerializer()
    tags = BOJTagDTOSerializer(many=True)
    hints = serializers.ListField(child=serializers.CharField())


class ProblemDTOSerializer(serializers.Serializer):
    problem_ref_id = serializers.IntegerField()
    title = serializers.CharField()
    analysis = ProblemAnalysisDTOSerializer()


class UnitDTOSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()


class ProblemLimitDTOSerializer(serializers.Serializer):
    value = serializers.FloatField()
    unit = UnitDTOSerializer()


class ProblemDetailDTOSerializer(ProblemDTOSerializer):
    link = serializers.URLField()
    description = serializers.CharField()
    input_description = serializers.CharField()
    output_description = serializers.CharField()
    memory_limit = ProblemLimitDTOSerializer()
    time_limit = ProblemLimitDTOSerializer()
    created_at = serializers.DateTimeField()


class ProblemDifficultyStatisticDTOSerializer(serializers.Serializer):
    difficulty = serializers.IntegerField()
    count = serializers.IntegerField()
    ratio = serializers.FloatField()


class ProblemTagStaticDTOSerializer(serializers.Serializer):
    tag = BOJTagDTOSerializer()
    count = serializers.IntegerField()
    ratio = serializers.FloatField()


class ProblemStatisticDTOSerializer(serializers.Serializer):
    problem_count = serializers.IntegerField()
    difficulties = ProblemDifficultyStatisticDTOSerializer(many=True)
    tags = ProblemTagStaticDTOSerializer(many=True)


class ProblemDAOSerializer(GenericModelToDTOSerializer[models.ProblemDAO, dto.ProblemDetailDTO]):
    model_converter_class = converters.ProblemDetailConverter
    dto_serializer_class = ProblemDetailDTOSerializer

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
        extra_kwargs = {
            models.ProblemDAO.field_name.CREATED_BY: {
                'read_only': True,
                'default': serializers.CurrentUserDefault(),
            },
        }


class ProblemSearchQueryParamSerializer(serializers.Serializer):
    q = serializers.CharField(required=False, default='')
