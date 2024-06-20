from rest_framework.serializers import *

from core.serializers import LanguageSerializer
from user.serializers import UserSerializer

from .models import *


class CrewSerializer(ModelSerializer):
    captain = UserSerializer(read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = '__all__'
