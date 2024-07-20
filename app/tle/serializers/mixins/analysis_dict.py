import typing

from rest_framework.serializers import *

from tle.models import Problem, ProblemAnalysis
from tle.models.choices import ProblemDifficulty
from tle.serializers.problem_tag import ProblemTagSerializer
from tle.serializers.mixins.difficulty_dict import DifficultyDictMixin


class AnalysisDictMixin(DifficultyDictMixin):
    def analysis_dict(self, problem: Problem) -> typing.Dict:
        try:
            return self._analysis_dict(problem.analysis)
        except ProblemAnalysis.DoesNotExist:
            return self._analysis_dict_default()

    def _analysis_dict(self, analysis: ProblemAnalysis):
        return {
            'difficulty': {
                "name_ko": ProblemDifficulty.get_name(analysis.difficulty, lang='ko'),
                "name_en": ProblemDifficulty.get_name(analysis.difficulty, lang='en'),
                'value': analysis.difficulty,
                'description': (
                    "기초적인 계산적 사고와 프로그래밍 문법만 있어도 해결 가능한 수준"
                    " [이 기능은 추가될 예정이 없습니다]"
                ),
            },
            'time_complexity': {
                'value': analysis.time_complexity,
                'description': (
                    "선형시간에 풀이가 가능한 문제. N의 크기에 주의하세요."
                    " [이 기능은 추가될 예정이 없습니다]"
                ),
            },
            'hint': analysis.hint,
            'tags': ProblemTagSerializer(analysis.tags, many=True).data,
            'is_analyzed': True,
        }

    def _analysis_dict_default(self):
        default_difficulty = 0  # Under analysis
        return {
            'difficulty': {
                "name_ko": ProblemDifficulty.get_name(default_difficulty, lang='ko'),
                "name_en": ProblemDifficulty.get_name(default_difficulty, lang='en'),
                'value': default_difficulty,
                'description': (
                    "AI가 분석을 진행하고 있어요!"
                    " [이 기능은 추가될 예정이 없습니다]"
                ),
            },
            'time_complexity': {
                'value': '',
                'description': (
                    "AI가 분석을 진행하고 있어요!"
                    " [이 기능은 추가될 예정이 없습니다]"
                ),
            },
            'hint': [],
            'tags': [],
            'is_analyzed': False,
        }
