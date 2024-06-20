from rest_framework.serializers import *

from .models import *


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'image',
            'username',
            'email',
        ]

    # TODO: BOJUser Serializer 연결
