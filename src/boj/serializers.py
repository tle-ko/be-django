from rest_framework.serializers import *

from boj.models import *


class BOJUserSerializer(ModelSerializer):
    class Meta:
        model = BOJUser
        fields = [
            'boj_id',
            'level',
            'is_verified',
        ]
        extra_kwargs = {
            'boj_id': {'read_only': True},
            'level': {'read_only': True},
            'is_verified': {'read_only': True},
        }


class BOJTagSerializer(ModelSerializer):
    class Meta:
        model = BOJTag
        fields =  [
            'boj_id',
        ]
        extra_kwargs = {
            'boj_id': {'read_only': True},
        }
