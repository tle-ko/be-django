from rest_framework.serializers import *

from tle.models import Problem, ProblemAnalysis
from tle.serializers.problem_difficulty import ProblemDifficultySerializer


class ProblemMinimalSerializer(ModelSerializer):
    difficulty = SerializerMethodField()

    class Meta:
        model = Problem
        fields = [
            'id',
            'title',
            'difficulty',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['__all__']

    def get_difficulty(self, obj: Problem):
        try:
            difficulty = obj.analysis.difficulty
        except ProblemAnalysis.DoesNotExist:
            difficulty = 0
        return ProblemDifficultySerializer(difficulty).data
