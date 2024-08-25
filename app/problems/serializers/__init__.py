from rest_framework import serializers

from problems import models
from problems.serializers import fields
from users.serializers import UserMinimalSerializer


class ProblemDetailSerializer(serializers.ModelSerializer):
    analysis = fields.AnalysisField(read_only=True)
    memory_limit = fields.MemoryLimitField(read_only=True)
    time_limit = fields.TimeLimitField(read_only=True)
    created_by = UserMinimalSerializer(read_only=True)

    class Meta:
        model = models.Problem
        fields = [
            'id',
            'analysis',
            'memory_limit',
            'time_limit',
            models.Problem.field_name.TITLE,
            models.Problem.field_name.LINK,
            models.Problem.field_name.DESCRIPTION,
            models.Problem.field_name.INPUT_DESCRIPTION,
            models.Problem.field_name.OUTPUT_DESCRIPTION,
            models.Problem.field_name.MEMORY_LIMIT,
            models.Problem.field_name.TIME_LIMIT,
            models.Problem.field_name.CREATED_AT,
            models.Problem.field_name.CREATED_BY,
            models.Problem.field_name.UPDATED_AT,
        ]
        read_only_fields = [
            'id',
            'analysis',
            'memory_limit',
            'time_limit',
            models.Problem.field_name.CREATED_AT,
            models.Problem.field_name.CREATED_BY,
            models.Problem.field_name.UPDATED_AT,
        ]
        extra_kwargs = {
            models.Problem.field_name.MEMORY_LIMIT: {'write_only': True},
            models.Problem.field_name.TIME_LIMIT: {'write_only': True},
        }

    def create(self, validated_data):
        validated_data[models.Problem.field_name.CREATED_BY] = serializers.CurrentUserDefault()(self)
        return super().create(validated_data)


class ProblemMinimalSerializer(serializers.ModelSerializer):
    difficulty = fields.DifficultyField(read_only=True)

    class Meta:
        model = models.Problem
        fields = [
            'id',
            models.Problem.field_name.TITLE,
            'difficulty',
            models.Problem.field_name.CREATED_AT,
            models.Problem.field_name.UPDATED_AT,
        ]
        read_only_fields = ['__all__']
