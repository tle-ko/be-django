from rest_framework.serializers import *

from tle.models import Problem
from tle.serializers.problem_analysis import ProblemAnalysisSerializer


class ProblemDetailSerializer(ModelSerializer):
    analysis= ProblemAnalysisSerializer(read_only=True)
    memory_limit_unit= SerializerMethodField()
    time_limit_unit= SerializerMethodField()

    class Meta:
        model= Problem
        fields= [
            'id',
            'analysis',
            'title',
            'link',
            'description',
            'input_description',
            'output_description',
            'memory_limit',
            'memory_limit_unit',
            'time_limit',
            'time_limit_unit',
            'created_at',
            'updated_at',
        ]
        extra_kwargs= {
            'id': {'read_only': True},
            'anaysis': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_memory_limit_unit(self, obj):
        return Problem.MEMORY_LIMIT_UNIT

    def get_time_limit_unit(self, obj):
        return Problem.TIME_LIMIT_UNIT
