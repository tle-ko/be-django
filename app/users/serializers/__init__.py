from rest_framework import serializers
from rest_framework.serializers import *

from users.models import User
from users.serializers.fields import UserBojField
from users.serializers.mixins import ReadOnlySerializerMixin


__all__ = (
    'UserSignInSerializer',
    'UserSignUpSerializer',
    'UserDetailSerializer',
    'UserMinimalSerializer',
    'UserEmailSerializer',
    'EmailCodeSerializer',
)


class EmailSerializer(serializers.Serializer):
    email = EmailField()


class EmailCodeSerializer(serializers.Serializer):
    email = EmailField()
    code = CharField()


class EmailTokenSerializer(serializers.Serializer):
    email = EmailField()
    token = CharField()


class SignInSerializer(serializers.Serializer):
    email = EmailField()
    password = CharField()


class SignUpSerializer(serializers.ModelSerializer):
    verification_token = CharField()

    class Meta:
        model = User
        fields = [
            User.field_name.EMAIL,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.PASSWORD,
            User.field_name.BOJ_USERNAME,
            'verification_token',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            User.field_name.EMAIL,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.BOJ_USERNAME,
            User.field_name.CREATED_AT,
            User.field_name.LAST_LOGIN,
        ]


class UserMinimalSerializer(ModelSerializer, ReadOnlySerializerMixin):
    class Meta:
        model = User
        fields = [
            'id',
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            User.field_name.PROFILE_IMAGE: {'read_only': True},
            User.field_name.USERNAME: {'read_only': True},
        }
