from rest_framework.serializers import *

from tle.models import (
    Problem,
    ProblemAnalysis,
    ProblemDifficulty,
    ProblemTag,
)
from tle.serializers.user_serializer import UserMinimalSerializer


__all__ = (
    'ProblemSerializer',
    'ProblemMinimalSerializer',
    'ProblemAnalysisSerializer',
    'ProblemTagSerializer',
)


class ProblemTagSerializer(ModelSerializer):
    parent = SerializerMethodField()

    class Meta:
        model = ProblemTag
        fields = [
            'parent',
            'key',
            'name_ko',
            'name_en',
        ]
        read_only_fields = ['__all__']

    def get_parent(self, obj: ProblemTag):
        if obj.parent is None:
            return None
        return ProblemTagSerializer(obj.parent).data


class ProblemDifficultySerializer(Serializer):
    name_en = SerializerMethodField()
    name_ko = SerializerMethodField()
    value = SerializerMethodField()

    def get_name_ko(self, choice: int):
        return self._get_obj(choice).get_name('ko')

    def get_name_en(self, choice: int):
        return self._get_obj(choice).get_name('en')

    def get_value(self, choice: int):
        return self._get_obj(choice).value

    def _get_obj(self, choice: int) -> ProblemDifficulty:
        return ProblemDifficulty(choice)


class ProblemAnalysisSerializer(ModelSerializer):
    tags = ProblemTagSerializer(many=True, read_only=True)
    difficulty = ProblemDifficultySerializer(read_only=True)

    class Meta:
        model = ProblemAnalysis
        fields = [
            'difficulty',
            'tags',
            'time_complexity',
            'hint',
            'created_at',
        ]
        read_only_fields = ['__all__']


class ProblemMinimalSerializer(ModelSerializer):
    created_by = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id',
            'title',
            'link',
            'created_at',
            'created_by',
            'updated_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'read_only': True},
            'link': {'read_only': True},
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class ProblemSerializer(ModelSerializer):
    analysis = ProblemAnalysisSerializer(read_only=True)
    memory_limit_unit = SerializerMethodField()
    time_limit_unit = SerializerMethodField()
    created_by = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = [
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
            'created_by',
            'updated_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'anaysis': {'read_only': True},
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_memory_limit_unit(self, obj: Problem):
        return {
            "name_ko": "메가 바이트",
            "name_en": "Mega Bytes",
            "abbr": "MB",
        }

    def get_time_limit_unit(self, obj: Problem):
        return {
            "name_ko": "초",
            "name_en": "Seconds",
            "abbr": "s",
        }
