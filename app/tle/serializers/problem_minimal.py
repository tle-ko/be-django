from rest_framework.serializers import *

from tle.models import Problem, ProblemAnalysis
from tle.serializers.mixins import DifficultyDictMixin


class ProblemMinimalSerializer(ModelSerializer, DifficultyDictMixin):
    difficulty = SerializerMethodField()

    class Meta:
        model = Problem
        fields = [
            'id',
            Problem.field_name.TITLE,
            'difficulty',
            Problem.field_name.CREATED_AT,
            Problem.field_name.UPDATED_AT,
        ]
        read_only_fields = ['__all__']

    def get_difficulty(self, obj: Problem):
        try:
            return self.difficulty_dict(obj.analysis.difficulty)
        except ProblemAnalysis.DoesNotExist:
            return self.difficulty_dict(0)
