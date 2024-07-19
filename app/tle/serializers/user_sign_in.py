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
        return self.boj_profile(obj)

    def create(self, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def update(self, instance, validated_data):
        raise PermissionDenied('Cannot create user through this serializer')

    def save(self, **kwargs):
        raise PermissionDenied('Cannot update user through this serializer')
