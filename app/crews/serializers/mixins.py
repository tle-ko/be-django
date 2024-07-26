from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import CurrentUserDefault, Field


class ReadOnlySerializerMixin:
    def create(self, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def update(self, instance, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def save(self, **kwargs):
        raise PermissionDenied('Cannot update user through this serializer')


class CurrentUserMixin(Field):
    def current_user(self):
        return CurrentUserDefault()(self)
