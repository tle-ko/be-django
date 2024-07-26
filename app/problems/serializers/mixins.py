from typing import Optional

from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import Field

from problems.models import Problem, ProblemAnalysis


class ReadOnlySerializerMixin:
    def create(self, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def update(self, instance, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def save(self, **kwargs):
        raise PermissionDenied('Cannot update user through this serializer')


class ReadOnlyFieldMixin(Field):
    def get_attribute(self, instance):
        return instance

    def to_internal_value(self, data):
        raise PermissionDenied('This field is read-only')


class AnalysisMixin:
    def get_analysis(self, problem: Problem) -> Optional[ProblemAnalysis]:
        try:
            return ProblemAnalysis.objects.filter(**{
                ProblemAnalysis.field_name.PROBLEM: problem,
            }).last()
        except ProblemAnalysis.DoesNotExist:
            return None
