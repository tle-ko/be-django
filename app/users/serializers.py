from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.validators import EmailValidator
from django.http.request import HttpRequest
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from boj.models import BOJUser
from boj.serializers import BOJUserSerializer
from users.models import User


PK = 'id'


# Username or Email Serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class IsEmailUsableField(serializers.BooleanField):
    def get_attribute(self, instance):
        assert 'email' in instance, instance
        assert isinstance(instance['email'], str)
        return not User.objects.filter(email=instance['email']).exists()


class IsEmailUsableSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_usable = IsEmailUsableField(read_only=True)


class IsUsernameUsableField(serializers.BooleanField):
    def get_attribute(self, instance):
        assert 'username' in instance, instance
        assert isinstance(instance['username'], str)
        return not User.objects.filter(username=instance['username']).exists()


class IsUsernameUsableSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_usable = IsUsernameUsableField()


class EmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class EmailTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()


# User Serializers

class BOJField(serializers.SerializerMethodField):
    def to_representation(self, value: BOJUser):
        return BOJUserSerializer(value).data

    def get_attribute(self, instance: User) -> BOJUser:
        assert isinstance(instance, User)
        return BOJUser.objects.get_by_username(instance.boj_username)


class SignInSerializer(serializers.ModelSerializer):
    boj = BOJField()

    class Meta:
        model = User
        fields = [
            PK,
            User.field_name.EMAIL,
            User.field_name.PASSWORD,
            User.field_name.USERNAME,
            User.field_name.PROFILE_IMAGE,
            User.field_name.TOKEN,
            User.field_name.REFRESH_TOKEN,
            'boj',
        ]
        extra_kwargs = {
            PK: {'read_only': True},
            User.field_name.EMAIL: {
                'write_only': True,
                'validators': [EmailValidator],
            },
            User.field_name.PASSWORD: {
                'write_only': True,
                'style': {'input_type': 'password'},
            },
            User.field_name.USERNAME: {'read_only': True},
            User.field_name.PROFILE_IMAGE: {'read_only': True},
            User.field_name.TOKEN: {'read_only': True},
            User.field_name.REFRESH_TOKEN: {'read_only': True},
        }

    def save(self, **kwargs):
        # 여기서는 사용자의 액세스 토큰 외의 정보를 수정하지는 않는다.
        request: HttpRequest = self.context['request']
        user: Optional[User]
        if (user := authenticate(request=request, **self.validated_data)) is None:
            raise AuthenticationFailed(f'Invalid email or password {self.validated_data}')
        login(request, user)
        user.rotate_token()
        self.instance = user


class SignUpSerializer(serializers.ModelSerializer):
    verification_token = serializers.CharField()

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
    boj = BOJField()

    class Meta:
        model = User
        fields = [
            PK,
            User.field_name.USERNAME,
            User.field_name.PROFILE_IMAGE,
            'boj',
        ]
        read_only_fields = ['__all__']


class UserUpdateSerializer(serializers.ModelSerializer):
    boj = BOJField()

    class Meta:
        model = User
        fields = [
            User.field_name.EMAIL,
            User.field_name.PASSWORD,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.BOJ_USERNAME,
            'boj',
        ]
        extra_kwargs = {
            User.field_name.EMAIL: {
                'read_only': True,
            },
            User.field_name.PASSWORD: {
                'write_only': True,
                'style': {'input_type': 'password'},
            },
            User.field_name.BOJ_USERNAME: {
                'write_only': True,
            }
        }

    def save(self, **kwargs):
        instance: User = super().save(**kwargs)
        if User.field_name.PASSWORD in self.validated_data:
            instance.set_password(self.validated_data[User.field_name.PASSWORD])
            instance.save()


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            PK,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
        ]
        read_only_fields = ['__all__']
