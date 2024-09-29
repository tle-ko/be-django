from rest_framework import serializers

from apps.boj.serializers import BOJTagDTOSerializer
from common.mixins import SerializerCurrentUserMixin

from . import models
from . import proxy


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


class ProblemDAOSerializer(SerializerCurrentUserMixin, serializers.ModelSerializer):
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

    def save(self, **kwargs):
        if self.is_creating():
            kwargs[models.ProblemDAO.field_name.CREATED_BY] = self.get_authenticated_user()
        return super().save(**kwargs)

    def is_creating(self) -> bool:
        return (self.instance is None) or (self.instance.created_by is None)

    @property
    def data(self):
        self.instance = proxy.Problem.objects.get(pk=self.instance.pk)
        return ProblemDetailDTOSerializer(self.instance.as_detail_dto()).data


class ProblemSearchQueryParamSerializer(serializers.Serializer):
    q = serializers.CharField(required=False, default=None)
