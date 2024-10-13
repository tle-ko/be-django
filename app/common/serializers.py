from __future__ import annotations

import typing

from rest_framework import serializers
from rest_framework.request import Request

from users.models import User

from . import converters


class GenericModelToDTOSerializer(serializers.ModelSerializer):
    model_converter_class: typing.Type[converters.ModelConverter] = None
    dto_serializer_class: typing.Type[serializers.Serializer] = None

    def get_model_converter(self, *args, **kwargs) -> converters.ModelConverter:
        if self.model_converter_class.user_required:
            return self.model_converter_class(self.get_authenticated_user(), *args, **kwargs)
        else:
            return self.model_converter_class(*args, **kwargs)

    def get_dto_serializer(self, *args, **kwargs) -> serializers.Serializer:
        return self.dto_serializer_class(*args, **kwargs)

    @property
    def data(self):
        obj = self.get_model_converter().instance_to_dto(self.instance)
        return self.get_dto_serializer(obj).data

    def get_request(self) -> Request:
        return self.context['request']

    def get_any_user(self) -> User:
        return self.get_request().user

    def get_authenticated_user(self) -> User:
        instance = self.get_any_user()
        assert instance.is_authenticated, 'The user must be authenticated'
        return instance
