from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import *

from tle.models import User, UserManager


__all__ = (
    'UserSerializer',
    'UserSignInSerializer',
    'UserMinimalSerializer',
)


class UserSerializer(ModelSerializer):
    boj = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'profile_image',
            'username',
            'password',
            'boj_username',
            'boj',
            'created_at',
            'last_login',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'boj': {'read_only': True},
            'created_at': {'read_only': True},
            'last_login': {'read_only': True},
            'password': {'write_only': True},
            'boj_username': {'write_only': True},
        }

    def get_boj(self, obj: User) -> dict:
        return {
            'username': obj.boj_username,
            'profile_url': f'https://boj.kr/{obj.boj_username}',
            'tier': obj.boj_tier,
            'tier_updated_at': obj.boj_tier_updated_at,
        }

    def create(self, validated_data):
        user_manager: UserManager = User.objects
        return user_manager.create_user(**validated_data)


class UserSignInSerializer(ModelSerializer):
    email = EmailField(write_only=True, validators=None)
    boj = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'profile_image',
            'username',
            'password',
            'boj',
            'created_at',
            'last_login',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'profile_image': {'read_only': True},
            'username': {'read_only': True},
            'boj': {'read_only': True},
            'created_at': {'read_only': True},
            'last_login': {'read_only': True},
            'password': {'write_only': True},
        }

    def get_boj(self, obj: User) -> dict:
        return {
            'username': obj.boj_username,
            'profile_url': f'https://boj.kr/{obj.boj_username}',
            'tier': obj.boj_tier,
            'tier_updated_at': obj.boj_tier_updated_at,
        }

    def create(self, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def update(self, instance, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def save(self, **kwargs):
        raise PermissionDenied('Cannot update user through this serializer')


class UserMinimalSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'profile_image',
            'username',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'profile_image': {'read_only': True},
            'username': {'read_only': True},
        }
