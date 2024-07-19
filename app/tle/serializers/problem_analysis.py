from rest_framework.serializers import *

from tle.models import ProblemAnalysis
from tle.serializers.problem_tag import ProblemTagSerializer
from tle.serializers.problem_difficulty import ProblemDifficultySerializer


class ProblemAnalysisSerializer(ModelSerializer):
    tags = ProblemTagSerializer(many=True, read_only=True)
    difficulty = ProblemDifficultySerializer(read_only=True)
    difficulty_description = SerializerMethodField()
    time_complexity_description = SerializerMethodField()

    class Meta:
        model = ProblemAnalysis
        fields = [
            'difficulty',
            'difficulty_description',
            'tags',
            'time_complexity',
            'time_complexity_description',
            'hint',
            'created_at',
        ]
        read_only_fields = ['__all__']

    def get_difficulty_description(self, obj: ProblemAnalysis):
        return (
            "[이 기능은 아직 추가할 예정이 없습니다] "
            "기초적인 계산적 사고와 프로그래밍 문법만 있어도 해결 가능한 수준"
        )

    def get_time_complexity_description(self, obj: ProblemAnalysis):
        return (
            "[이 기능은 아직 추가할 예정이 없습니다] "
            "선형시간에 풀이가 가능한 문제. N의 크기에 주의하세요."
        )
