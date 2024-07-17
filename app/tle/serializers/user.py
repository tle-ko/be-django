from rest_framework.serializers import *

from tle.models import User


class BOJ_Mixin:
    def get_boj(self, obj: User) -> dict:
        return {
            'username': obj.boj_username,
            'tier': obj.boj_tier,
            'tier_updated_at': obj.boj_tier_updated_at,
        }


USER_SERIALIZER_FIELDS = {
    'id': {'read_only': True},
    'profile_image': {'read_only': True},
    'username': {'read_only': True},
    'boj': {'read_only': True},
}


class UserSerializer(ModelSerializer, BOJ_Mixin):
    boj = SerializerMethodField()

    class Meta:
        model = User
        fields = USER_SERIALIZER_FIELDS.keys()
        extra_kwargs = USER_SERIALIZER_FIELDS


USER_SIGN_IN_SERIALIZER_FIELDS = {
    **USER_SERIALIZER_FIELDS,
    'email': {},
    'password': {'write_only': True},
}


class UserSignInSerializer(ModelSerializer, BOJ_Mixin):
    boj = SerializerMethodField()

    class Meta:
        model = User
        fields = USER_SIGN_IN_SERIALIZER_FIELDS.keys()
        extra_kwargs = USER_SIGN_IN_SERIALIZER_FIELDS


USER_SIGN_UP_SERIALIZER_FIELDS = {
    'id': {'read_only': True},
    'boj': {'read_only': True},

    'email': {},
    'password': {'write_only': True},
    'profile_image': {},
    'username': {},
    'boj_username': {'write_only': True},
}


class UserSignUpSerializer(ModelSerializer):
    boj = SerializerMethodField()

    class Meta:
        model = User
        fields = USER_SIGN_UP_SERIALIZER_FIELDS.keys()
        extra_kwargs = USER_SIGN_UP_SERIALIZER_FIELDS
