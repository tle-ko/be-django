from rest_framework.serializers import ModelSerializer

from account.serializers import UserSerializer

from ..models import Problem


class ProblemSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id',
            'title',
            'link',
            'description',
            'input_description',
            'output_description',
            'memory_limit',
            'time_limit',
            'user',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }
