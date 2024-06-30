from rest_framework.serializers import ModelSerializer

from ..models import Analysis
from ..serializers import TagSerializer


class AnalysisSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Analysis
        fields = [
            'id',
            'problem',
            'difficulty',
            'tags',
            'time_complexity',
            'created_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'problem': {'read_only': True},
            'created_at': {'read_only': True},
        }
