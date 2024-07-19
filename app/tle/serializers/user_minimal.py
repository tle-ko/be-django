from rest_framework.serializers import *

from tle.models import User


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
