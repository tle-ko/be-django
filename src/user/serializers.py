from rest_framework.serializers import *

from boj.serializers import BOJUserSerializer

from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'image',
            'username',
        ]

    # TODO: BOJUser Serializer 연결


class UserSignInSerializer(ModelSerializer):
    email = EmailField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'image',
            'username',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'image': {'read_only': True},
            'username': {'read_only': True},
            'email': {'write_only': True},
            'password': {'write_only': True},
        }


class UserSignUpSerializer(ModelSerializer):
    boj_id = CharField(max_length=40, required=False)
    boj_user = BOJUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'boj_id',
            'boj_user',
            'image',
            'username',
            'email',
            'password',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'boj_id': {'write_only': True},
            'boj_user': {'read_only': True},
            'password': {'write_only': True},
        }
