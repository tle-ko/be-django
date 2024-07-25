from rest_framework.serializers import *

from tle.models import User, UserManager
from tle.serializers.mixins import BojProfileMixin


class UserDetailSerializer(ModelSerializer, BojProfileMixin):
    boj = SerializerMethodField(read_only=True)

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

    def get_boj(self, obj: User) -> dict:
        return self.boj_profile(obj)

    def create(self, validated_data):
        user_manager: UserManager = User.objects
        return user_manager.create_user(**validated_data)
