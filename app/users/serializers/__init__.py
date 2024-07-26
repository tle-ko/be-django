from rest_framework.serializers import *

from users.models import User
from users.serializers.fields import UserBojField
from users.serializers.mixins import ReadOnlySerializerMixin


class UserSignInSerializer(ModelSerializer, ReadOnlySerializerMixin):
    email = EmailField(write_only=True, validators=None)
    boj = UserBojField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            User.field_name.EMAIL,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.PASSWORD,
            'boj',
            User.field_name.CREATED_AT,
            User.field_name.LAST_LOGIN,
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'boj': {'read_only': True},
            User.field_name.PROFILE_IMAGE: {'read_only': True},
            User.field_name.USERNAME: {'read_only': True},
            User.field_name.CREATED_AT: {'read_only': True},
            User.field_name.LAST_LOGIN: {'read_only': True},
            User.field_name.PASSWORD: {'write_only': True},
        }


class UserDetailSerializer(ModelSerializer, ReadOnlySerializerMixin):
    boj = UserBojField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            User.field_name.EMAIL,
            User.field_name.PROFILE_IMAGE,
            User.field_name.USERNAME,
            User.field_name.PASSWORD,
            User.field_name.BOJ_USERNAME,
            'boj',
            User.field_name.CREATED_AT,
            User.field_name.LAST_LOGIN,
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'boj': {'read_only': True},
            User.field_name.CREATED_AT: {'read_only': True},
            User.field_name.LAST_LOGIN: {'read_only': True},
            User.field_name.PASSWORD: {'write_only': True},
            User.field_name.BOJ_USERNAME: {'write_only': True},
        }


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
