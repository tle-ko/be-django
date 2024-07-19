from rest_framework.serializers import *

from tle.models import CrewMember
from tle.serializers.user_minimal import UserMinimalSerializer


class CrewMemberSerializer(ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    is_captain = SerializerMethodField()

    class Meta:
        model = CrewMember
        fields = (
            'user',
            'is_captain',
        )

    def get_is_captain(self, obj: CrewMember) -> bool:
        return obj.crew.captain == obj.user
