from rest_framework.serializers import (
    ModelSerializer,
)

from core.serializers import LanguageSerializer
from crew.models import Crew
from crew.serializers.crew_member import CrewMemberSerializer


class CrewSerializer(ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = '__all__'
