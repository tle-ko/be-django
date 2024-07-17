from rest_framework.serializers import ModelSerializer

from tle.models import Problem
from tle.serializers.user import UserSerializer


PROBLEM_SERIALIZER_FIELDS = {
    'id': {'read_only': True},
    'title': {},
    'link': {},
    'description': {},
    'input_description': {},
    'output_description': {},
    'memory_limit': {},
    'time_limit': {},
    'created_at': {'read_only': True},
    'created_by': {'read_only': True},
    'updated_at': {'read_only': True},
}


class ProblemSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = PROBLEM_SERIALIZER_FIELDS.keys()
        extra_kwargs = PROBLEM_SERIALIZER_FIELDS
