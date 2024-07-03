from rest_framework.serializers import ModelSerializer

from account.serializers import UserSerializer

from ..models import Problem
from ..serializers.problem_analysis import ProblemAnalysisSerializer


class ProblemSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    analysis = ProblemAnalysisSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id',
            'analysis',
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
            'analysis': {'read_only': True},
            'user': {'read_only': True},
        }
