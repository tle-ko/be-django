from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from crew.models import CrewMember
from user.serializers import UserSerializer


class CrewMemberSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    is_captain = SerializerMethodField()

    class Meta:
        model = CrewMember
        fields = (
            'user',
            'is_captain',
        )

    def get_is_captain(self, obj: CrewMember) -> bool:
        return obj.crew.captain == obj.user
