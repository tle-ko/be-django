from rest_framework import serializers

from boj.enums import BOJLevel
from boj.serializers import BOJUserSerializer
from boj.services import get_boj_user_service
from users.models import User


class UserBOJField(serializers.SerializerMethodField):
    def to_representation(self, instance: User):
        assert isinstance(instance, User)
        service = get_boj_user_service(instance.boj_username)
        return BOJUserSerializer(service.instance).data


class UserBOJLevelNameField(serializers.SerializerMethodField):
    def to_representation(self, instance: User):
        assert isinstance(instance, User)
        service = get_boj_user_service(instance.boj_username)
        level = BOJLevel(service.instance.level)
        return {
            'value': level.value,
            'name': level.get_name(),
        }


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
    boj = UserBOJField()

    class Meta:
        model = User
        fields = [
            'id',
            User.field_name.USERNAME,
            User.field_name.PROFILE_IMAGE,
            'boj',
        ]
        read_only_fields = ['__all__']


class UserUpdateSerializer(serializers.ModelSerializer):
    level = UserBOJLevelNameField()

    class Meta:
        model = User
        fields = [
            User.field_name.EMAIL,
            User.field_name.PASSWORD,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.BOJ_USERNAME,
            'level',
        ]
        extra_kwargs = {
            User.field_name.EMAIL: {
                'read_only': True,
            },
            User.field_name.PASSWORD: {
                'write_only': True,
            }
        }


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
        ]
        read_only_fields = ['__all__']
