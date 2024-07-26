from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import Field


class ReadOnlySerializerMixin:
    def create(self, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def update(self, instance, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def save(self, **kwargs):
        raise PermissionDenied('Cannot update user through this serializer')


class ReadOnlyField(Field):
    def get_attribute(self, instance):
        return instance

    def to_internal_value(self, data):
        raise PermissionDenied('This field is read-only')
