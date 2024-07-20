import typing

from rest_framework.serializers import *

from tle.models.choices import ProblemDifficulty


class DifficultyDictMixin:
    def difficulty_dict(self, difficulty: ProblemDifficulty) -> typing.Dict:
        return {
            "name_ko": ProblemDifficulty.get_name(difficulty.value, lang='ko'),
            "name_en": ProblemDifficulty.get_name(difficulty.value, lang='en'),
            "value": difficulty.value,
        }
