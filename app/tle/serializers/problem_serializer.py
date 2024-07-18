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

    def get_name_ko(self, value: int):
        return ProblemDifficulty.get_name(value, 'ko')

    def get_name_en(self, value: int):
        return ProblemDifficulty.get_name(value, 'en')

    def get_value(self, value: int):
        return value


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
    difficulty = SerializerMethodField()

    class Meta:
        model = Problem
        fields = [
            'id',
            'title',
            'link',
            'difficulty',
            'created_at',
            'created_by',
            'updated_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'read_only': True},
            'link': {'read_only': True},
            'difficulty': {'read_only': True},
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_difficulty(self, obj: Problem):
        try:
            difficulty = obj.analysis.difficulty
        except ProblemAnalysis.DoesNotExist:
            difficulty = 0
        return ProblemDifficultySerializer(difficulty).data


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
