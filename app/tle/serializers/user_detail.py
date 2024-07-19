from rest_framework.serializers import *

from tle.models import User, UserManager


class UserDetailSerializer(ModelSerializer):
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
