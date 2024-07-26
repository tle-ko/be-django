from rest_framework.serializers import ModelSerializer

from problems.constants import Unit
from problems.models import Problem, ProblemDifficulty, ProblemTag
from problems.serializers.mixins import ReadOnlyFieldMixin, AnalysisMixin


class MemoryLimitField(ReadOnlyFieldMixin):
    def to_representation(self, problem: Problem):
        return {
            "value": problem.memory_limit_megabyte,
            "unit": {
                "name_ko": Unit.MEGA_BYTE.name_ko,
                "name_en": Unit.MEGA_BYTE.name_en,
                "abbr": Unit.MEGA_BYTE.abbr,
            },
        }


class TimeLimitField(ReadOnlyFieldMixin):
    def to_representation(self, problem: Problem):
        return {
            "value": problem.time_limit_second,
            "unit": {
                "name_ko": Unit.SECOND.name_ko,
                "name_en": Unit.SECOND.name_en,
                "abbr": Unit.SECOND.abbr,
            },
        }


class DifficultyField(ReadOnlyFieldMixin, AnalysisMixin):
    def to_representation(self, problem: Problem):
        if (analysis := self.get_analysis(problem)) is None:
            difficulty = ProblemDifficulty.UNDER_ANALYSIS
        else:
            difficulty = ProblemDifficulty(analysis.difficulty)
        return {
            "name_ko": difficulty.get_name(lang='ko'),
            "name_en": difficulty.get_name(lang='en'),
            'value': difficulty.value,
        }


class AnalysisField(ReadOnlyFieldMixin, AnalysisMixin):
    def to_representation(self, problem: Problem):
        if (analysis := self.get_analysis(problem)) is None:
            difficulty = ProblemDifficulty.UNDER_ANALYSIS
            difficulty_description = "AI가 분석을 진행하고 있어요! [이 기능은 추가될 예정이 없습니다]"
            time_complexity = ''
            time_complexity_description = "AI가 분석을 진행하고 있어요! [이 기능은 추가될 예정이 없습니다]"
            hint = []
            tags = []
            is_analyzed = False
        else:
            difficulty = ProblemDifficulty(analysis.difficulty)
            difficulty_description = "기초적인 계산적 사고와 프로그래밍 문법만 있어도 해결 가능한 수준 [이 기능은 추가될 예정이 없습니다]"
            time_complexity = analysis.time_complexity
            time_complexity_description = "선형시간에 풀이가 가능한 문제. N의 크기에 주의하세요. [이 기능은 추가될 예정이 없습니다]"
            hint = analysis.hint
            tags = ProblemTagSerializer(analysis.tags, many=True).data
            is_analyzed = True
        return {
            'difficulty': {
                "name_ko": difficulty.get_name(lang='ko'),
                "name_en": difficulty.get_name(lang='en'),
                'value': difficulty.value,
                'description': difficulty_description,
            },
            'time_complexity': {
                'value': time_complexity,
                'description': time_complexity_description,
            },
            'hint': hint,
            'tags': tags,
            'is_analyzed': is_analyzed,
        }


class ProblemTagSerializer(ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = [
            ProblemTag.field_name.KEY,
            ProblemTag.field_name.NAME_KO,
            ProblemTag.field_name.NAME_EN,
        ]
        read_only_fields = ['__all__']
