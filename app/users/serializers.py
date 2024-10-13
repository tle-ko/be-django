from django.contrib import auth
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.boj.serializers import BOJUserDTOSerializer
from common.serializers import GenericModelToDTOSerializer

from . import converters
from . import dto
from . import models


PK = 'id'


Serializer = serializers.Serializer


class UserDTOSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    profile_image = serializers.CharField()


class UserDetailDTOSerializer(UserDTOSerializer):
    email = serializers.EmailField()
    boj = BOJUserDTOSerializer()


class UserCredentialDTOSerializer(UserDTOSerializer):
    token = serializers.CharField()


class UserDAOSerializer(GenericModelToDTOSerializer[models.User, dto.UserDetailDTO]):
    model_converter_class = converters.UserDetailConverter
    dto_serializer_class = UserDetailDTOSerializer

    class Meta:
        model = models.User
        fields = [
            models.User.field_name.PASSWORD,
            models.User.field_name.USERNAME,
            models.User.field_name.BOJ_USERNAME,
            models.User.field_name.PROFILE_IMAGE,
        ]
        extra_kwargs = {
            models.User.field_name.PASSWORD: {'style': {'input_type': 'password'}},
        }

    def is_valid(self, *, raise_exception=False):
        if models.User.field_name.EMAIL in self.initial_data:
            if raise_exception:
                raise serializers.ValidationError('이메일은 수정할 수 없습니다.')
            return False
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        instance: models.User = super().save(**kwargs)
        validated_data = {**self.validated_data, **kwargs}
        if models.User.field_name.PASSWORD in validated_data:
            new_password = validated_data[models.User.field_name.PASSWORD]
            instance.set_password(new_password)
            instance.save()
        if models.User.field_name.BOJ_USERNAME in validated_data:
            instance.get_boj_user().update_async()


class UserDAOSignInSerializer(GenericModelToDTOSerializer[models.User, dto.UserDTO]):
    model_converter_class = converters.UserCredentialConverter
    dto_serializer_class = UserCredentialDTOSerializer

    class Meta:
        model = models.User
        fields = [
            models.User.field_name.EMAIL,
            models.User.field_name.PASSWORD,
        ]
        extra_kwargs = {
            models.User.field_name.EMAIL: {'validators': [EmailValidator]},
            models.User.field_name.PASSWORD: {'style': {'input_type': 'password'}},
        }

    def create(self, validated_data: dict):
        instance: models.User
        instance = auth.authenticate(self.get_request(), **validated_data)
        if instance is None:
            raise serializers.ValidationError('이메일 혹은 비밀번호가 올바르지 않습니다.')
        auth.login(self.get_request(), instance)
        instance.rotate_token()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        raise NotImplementedError


class UserDAOSignUpSerializer(GenericModelToDTOSerializer[models.User, dto.UserDTO]):
    model_converter_class = converters.UserConverter
    dto_serializer_class = UserDTOSerializer

    verification_token = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = [
            models.User.field_name.EMAIL,
            models.User.field_name.PASSWORD,
            models.User.field_name.USERNAME,
            models.User.field_name.BOJ_USERNAME,
            models.User.field_name.PROFILE_IMAGE,
            'verification_token',
        ]
        extra_kwargs = {
            models.User.field_name.PASSWORD: {'style': {'input_type': 'password'}},
        }

    def is_valid(self, *, raise_exception=False):
        if not super().is_valid(raise_exception=raise_exception):
            return False
        email: str = self.validated_data['email']
        token: str = self.validated_data.pop('verification_token')
        try:
            instance: models.UserEmailVerification
            instance = models.UserEmailVerification.objects.get(**{
                models.UserEmailVerification.field_name.EMAIL: email,
            })
            assert instance.verification_token == token
        except models.UserEmailVerification.DoesNotExist:
            self._validated_data = {}
            self._errors = {'verification_token': ['이메일 인증 토큰이 발급되지 않았습니다.']}
        except AssertionError:
            self._validated_data = {}
            self._errors = {'verification_token': ['이메일 인증 토큰이 올바르지 않습니다.']}
        else:
            self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)

    def save(self, **kwargs):
        instance: models.User = super().save(**kwargs)
        validated_data = {**self.validated_data, **kwargs}
        if models.User.field_name.PASSWORD in validated_data:
            new_password = validated_data[models.User.field_name.PASSWORD]
            instance.set_password(new_password)
            instance.save()
        if models.User.field_name.BOJ_USERNAME in validated_data:
            instance.get_boj_user().update_async()

    def update(self, instance, validated_data):
        raise NotImplementedError


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
            data['is_usable'] = not models.User.objects.filter(email=email).exists()
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
            data['is_usable'] = not models.User.objects.filter(username=name).exists()
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
        model = models.UserEmailVerification
        fields = [
            models.UserEmailVerification.field_name.EMAIL,
            models.UserEmailVerification.field_name.VERIFICATION_CODE,
            models.UserEmailVerification.field_name.VERIFICATION_TOKEN,
            models.UserEmailVerification.field_name.EXPIRES_AT,
        ]
        extra_kwargs = {
            models.UserEmailVerification.field_name.EMAIL: {'validators': [EmailValidator]},
            models.UserEmailVerification.field_name.VERIFICATION_CODE: {'write_only': True},
            models.UserEmailVerification.field_name.VERIFICATION_TOKEN: {'read_only': True},
            models.UserEmailVerification.field_name.EXPIRES_AT: {'read_only': True},
        }

    def update(self, instance: models.UserEmailVerification, validated_data: dict):
        verification_code = validated_data.get(
            models.UserEmailVerification.field_name.VERIFICATION_CODE, None)
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


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()
