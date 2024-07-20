from rest_framework.serializers import *

from tle.enums import Unit
from tle.models import Problem
from tle.serializers.mixins import AnalysisDictMixin


class ProblemDetailSerializer(ModelSerializer, AnalysisDictMixin):
    analysis = SerializerMethodField()
    memory_limit = SerializerMethodField()
    time_limit = SerializerMethodField()

    class Meta:
        model = Problem
        fields = [
            'id',
            'analysis',
            'memory_limit',
            'time_limit',
            Problem.field_name.TITLE,
            Problem.field_name.LINK,
            Problem.field_name.DESCRIPTION,
            Problem.field_name.INPUT_DESCRIPTION,
            Problem.field_name.OUTPUT_DESCRIPTION,
            Problem.field_name.MEMORY_LIMIT_MEGABYTE,
            Problem.field_name.TIME_LIMIT_SECOND,
            Problem.field_name.CREATED_AT,
            Problem.field_name.UPDATED_AT,
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'analysis': {'read_only': True},
            'memory_limit': {'read_only': True},
            'time_limit': {'read_only': True},
            Problem.field_name.CREATED_AT: {'read_only': True},
            Problem.field_name.UPDATED_AT: {'read_only': True},
            Problem.field_name.MEMORY_LIMIT_MEGABYTE: {'write_only': True},
            Problem.field_name.TIME_LIMIT_SECOND: {'write_only': True},
        }

    def get_analysis(self, obj: Problem):
        return self.analysis_dict(obj)

    def get_memory_limit(self, obj: Problem):
        return {
            "value": obj.memory_limit_megabyte,
            "name_ko": Unit.MEGA_BYTE.name_ko,
            "name_en": Unit.MEGA_BYTE.name_en,
            "abbr": Unit.MEGA_BYTE.abbr,
        }

    def get_time_limit(self, obj: Problem):
        return {
            "value": obj.time_limit_second,
            "name_ko": Unit.SECOND.name_ko,
            "name_en": Unit.SECOND.name_en,
            "abbr": Unit.SECOND.abbr,
        }
