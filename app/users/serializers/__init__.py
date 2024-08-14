from rest_framework import serializers

from users.models import User
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
    email = serializers.EmailField()


class EmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class EmailTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SignUpSerializer(serializers.ModelSerializer):
    verification_token = serializers.CharField(read_only=True)

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


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()


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


class UserMinimalSerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
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
