from __future__ import annotations

import typing

from rest_framework import serializers

from users.models import User


class SerializerCurrentUserMixin:
    def get_any_user(self: typing.Union[SerializerCurrentUserMixin, serializers.Serializer]) -> User:
        return self.context['request'].user

    def get_authenticated_user(self: typing.Union[SerializerCurrentUserMixin, serializers.Serializer]) -> User:
        instance = self.get_any_user()
        assert instance.is_authenticated, 'The user must be authenticated'
        return instance
