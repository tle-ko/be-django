from rest_framework.serializers import *

from tle.models import Problem
from tle.serializers.mixins import AnalysisDictMixin


class ProblemDetailSerializer(ModelSerializer, AnalysisDictMixin):
    analysis = SerializerMethodField()
    memory_limit_unit = SerializerMethodField()
    time_limit_unit = SerializerMethodField()

    class Meta:
        model = Problem
        fields = [
            'id',
            'analysis',
            Problem.field_name.TITLE,
            Problem.field_name.LINK,
            Problem.field_name.DESCRIPTION,
            Problem.field_name.INPUT_DESCRIPTION,
            Problem.field_name.OUTPUT_DESCRIPTION,
            Problem.field_name.MEMORY_LIMIT,
            'memory_limit_unit',
            Problem.field_name.TIME_LIMIT,
            'time_limit_unit',
            Problem.field_name.CREATED_AT,
            Problem.field_name.UPDATED_AT,
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            Problem.field_name.ANALYSIS: {'read_only': True},
            'memory_limit_unit': {'read_only': True},
            'time_limit_unit': {'read_only': True},
            Problem.field_name.CREATED_AT: {'read_only': True},
            Problem.field_name.UPDATED_AT: {'read_only': True},
        }

    def get_analysis(self, obj: Problem):
        return self.analysis_dict(obj)

    def get_memory_limit_unit(self, obj):
        return Problem.MEMORY_LIMIT_UNIT

    def get_time_limit_unit(self, obj):
        return Problem.TIME_LIMIT_UNIT
