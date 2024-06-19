from rest_framework.serializers import *

from core.serializers import TagSerializer
from user.serializers import UserSerializer

from .models import *


class ProblemAnalysisSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = ProblemAnalysis
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'problem': {'write_only': True},
        }


class ProblemSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    analysis = ProblemAnalysisSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
