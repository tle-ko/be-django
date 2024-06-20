from rest_framework.serializers import *

from core.serializers import TagSerializer
from user.serializers import UserSerializer

from .models import *


class ProblemAnalysisSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = ProblemAnalysis
        fields = [
            'id',
            'problem',
            'difficulty',
            'tags',
            'time_complexity',
            'created_at',
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
        }


class ProblemSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    analysis = ProblemAnalysisSerializer(many=True, read_only=True)

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
