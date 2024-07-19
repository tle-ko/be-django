from rest_framework.serializers import *

from tle.models.choices import ProblemDifficulty


class ProblemDifficultySerializer(Serializer):
    name_en = SerializerMethodField()
    name_ko = SerializerMethodField()
    value = SerializerMethodField()

    def get_name_ko(self, value: int):
        return ProblemDifficulty.get_name(value, 'ko')

    def get_name_en(self, value: int):
        return ProblemDifficulty.get_name(value, 'en')

    def get_value(self, value: int):
        return value
