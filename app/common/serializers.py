from __future__ import annotations

import typing

from rest_framework import serializers

from users.models import User


class GenericModelSerializer(serializers.ModelSerializer):
    serializer_class: serializers.Serializer = None

    def get_any_user(self) -> User:
        return self.context['request'].user

    def get_authenticated_user(self) -> User:
        instance = self.get_any_user()
        assert instance.is_authenticated, 'The user must be authenticated'
        return instance

    def get_serializer(self, *args, **kwargs) -> typing.Optional[serializers.Serializer]:
        if self.serializer_class is None:
            return None
        return self.serializer_class(*args, **kwargs)

    def get_object(self):
        return self.instance

    @property
    def data(self):
        return self.get_serializer(self.get_object()).data
