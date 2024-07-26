from rest_framework.serializers import CurrentUserDefault, ModelSerializer

from problems.models import Problem
from problems.serializers.fields import (
    AnalysisField,
    MemoryLimitField,
    TimeLimitField,
    DifficultyField,
)
from problems.serializers.mixins import ReadOnlySerializerMixin
from users.serializers import UserMinimalSerializer


class ProblemDetailSerializer(ModelSerializer):
    analysis = AnalysisField(read_only=True)
    memory_limit = MemoryLimitField(read_only=True)
    time_limit = TimeLimitField(read_only=True)
    created_by = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id',
            'analysis',
            'memory_limit',
            'time_limit',
            Problem.field_name.TITLE,
            Problem.field_name.LINK,
            Problem.field_name.DESCRIPTION,
            Problem.field_name.INPUT_DESCRIPTION,
            Problem.field_name.OUTPUT_DESCRIPTION,
            Problem.field_name.MEMORY_LIMIT_MEGABYTE,
            Problem.field_name.TIME_LIMIT_SECOND,
            Problem.field_name.CREATED_AT,
            Problem.field_name.CREATED_BY,
            Problem.field_name.UPDATED_AT,
        ]
        read_only_fields = [
            'id',
            'analysis',
            'memory_limit',
            'time_limit',
            Problem.field_name.CREATED_AT,
            Problem.field_name.CREATED_BY,
            Problem.field_name.UPDATED_AT,
        ]
        extra_kwargs = {
            Problem.field_name.MEMORY_LIMIT_MEGABYTE: {'write_only': True},
            Problem.field_name.TIME_LIMIT_SECOND: {'write_only': True},
        }

    def create(self, validated_data):
        validated_data[Problem.field_name.CREATED_BY] = CurrentUserDefault()(
            self)
        return super().create(validated_data)


class ProblemMinimalSerializer(ModelSerializer, ReadOnlySerializerMixin):
    difficulty = DifficultyField(read_only=True)

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
