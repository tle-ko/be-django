from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.boj.serializers import BOJUserDTOSerializer

from . import converters
from users.models import User
from users.models import UserEmailVerification


PK = 'id'


class UserDTOSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    profile_image = serializers.CharField()


class UserManageDTOSerializer(UserDTOSerializer):
    email = serializers.EmailField()
    boj = BOJUserDTOSerializer()


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

class SignInSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = User
        fields = [
            PK,
            User.field_name.USERNAME,
            User.field_name.PROFILE_IMAGE,
        ]
        read_only_fields = ['__all__']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            User.field_name.EMAIL,
            User.field_name.PASSWORD,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.BOJ_USERNAME,
        ]
        extra_kwargs = {
            User.field_name.PASSWORD: {'style': {'input_type': 'password'}},
        }

    @property
    def data(self):
        obj = converters.UserConverter().instance_to_manage_dto(self.instance)
        return UserManageDTOSerializer(obj).data

    def is_valid(self, *, raise_exception=False):
        try:
            assert User.field_name.EMAIL not in self.initial_data, (
                '이메일은 수정할 수 없습니다.'
            )
        except AssertionError as exception:
            if raise_exception:
                raise ValidationError(exception)
            else:
                return (False, None)
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        self.instance: User = super().save(**kwargs)
        if User.field_name.PASSWORD in self.validated_data:
            self.instance.set_password(self.validated_data[User.field_name.PASSWORD])
            self.instance.save()


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            PK,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
        ]
        read_only_fields = ['__all__']
