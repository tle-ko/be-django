from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.validators import EmailValidator
from django.http.request import HttpRequest
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError

from boj.models import BOJUser
from boj.serializers import BOJUserSerializer
from users.models import User
from users.models import UserEmailVerification


PK = 'id'


# Username or Email Serializers

class UsabilityEmailField(serializers.Serializer):
    value = serializers.EmailField(read_only=True)
    is_usable = serializers.BooleanField(read_only=True)

    def get_attribute(self, instance):
        data = {
            'value': None,
            'is_usable': False,
        }
        if 'email' in instance:
            email = instance['email']
            data['value'] = email
            data['is_usable'] = not User.objects.filter(email=email).exists()
        return data


class UsabilityUsernameField(serializers.Serializer):
    value = serializers.CharField(read_only=True)
    is_usable = serializers.BooleanField(read_only=True)

    def get_attribute(self, instance):
        data = {
            'value': None,
            'is_usable': False,
        }
        if 'username' in instance:
            name = instance['username']
            data['value'] = name
            data['is_usable'] = not User.objects.filter(username=name).exists()
        return data


class UsabilitySerializerForQueryParameter(serializers.Serializer):
    email = serializers.EmailField(default=None)
    username = serializers.CharField(default=None)


class UsabilitySerializer(serializers.Serializer):
    email = UsabilityEmailField(default=None)
    username = UsabilityUsernameField(default=None)

    def to_representation(self, instance: dict):
        if (instance.get('email', None) is None) and (instance.get('username', None) is None):
            raise ValidationError('이메일 혹은 사용자명 중 하나는 주어져야 합니다.')
        return super().to_representation(instance)


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


# Email Validation Serializers

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmailVerification
        fields = [
            UserEmailVerification.field_name.EMAIL,
            UserEmailVerification.field_name.VERIFICATION_CODE,
            UserEmailVerification.field_name.VERIFICATION_TOKEN,
            UserEmailVerification.field_name.EXPIRES_AT,
        ]
        extra_kwargs = {
            UserEmailVerification.field_name.EMAIL: {'validators': [EmailValidator]},
            UserEmailVerification.field_name.VERIFICATION_CODE: {'write_only': True},
            UserEmailVerification.field_name.VERIFICATION_TOKEN: {'read_only': True},
            UserEmailVerification.field_name.EXPIRES_AT: {'read_only': True},
        }

    def update(self, instance: UserEmailVerification, validated_data: dict):
        verification_code = validated_data.get(
            UserEmailVerification.field_name.VERIFICATION_CODE, None)
        if verification_code is None:
            # 코드가 없다면 코드를 만들어 주자.
            instance.revoke_token()
            instance.rotate_code()
        else:
            # 인증 코드가 있다면 검증해주자.
            instance.is_valid_code(verification_code, raise_exception=True)
            instance.revoke_code()
            instance.rotate_token()
        instance.save()
        return instance


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
    verification_token = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            PK,
            User.field_name.EMAIL,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.PASSWORD,
            User.field_name.BOJ_USERNAME,
            'verification_token',
        ]
        extra_kwargs = {
            PK: {'read_only': True},
            User.field_name.EMAIL: {'write_only': True},
            User.field_name.PASSWORD: {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def create(self, validated_data: dict):
        email = validated_data.get('email')
        verification_token = validated_data.pop('verification_token')
        try:
            email_verification = UserEmailVerification.objects.get(email=email)
        except UserEmailVerification.DoesNotExist:
            raise ValidationError('이메일 인증 토큰이 발급되지 않았습니다.')
        if email_verification.verification_token != verification_token:
            raise ValidationError('이메일 인증 토큰이 올바르지 않습니다.')
        return super().create(validated_data)


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
