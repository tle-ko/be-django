from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import *

from tle.models import User
from tle.serializers.mixins import BojProfileMixin


class UserSignInSerializer(ModelSerializer, BojProfileMixin):
    email = EmailField(write_only=True, validators=None)
    boj = SerializerMethodField()

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

    def get_boj(self, obj: User) -> dict:
        return self.boj_profile(obj)

    def create(self, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def update(self, instance, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def save(self, **kwargs):
        raise PermissionDenied('Cannot update user through this serializer')
