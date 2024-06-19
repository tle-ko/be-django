from rest_framework.serializers import *

from user.serializers import UserSerializer

from .models import *


class ProblemSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
