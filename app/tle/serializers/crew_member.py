from rest_framework.serializers import *

from tle.models import CrewMember
from tle.serializers.user_minimal import UserMinimalSerializer


class CrewMemberSerializer(ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    is_captain = SerializerMethodField()

    class Meta:
        model = CrewMember
        fields = (
            CrewMember.field_name.USER,
            'is_captain',
            CrewMember.field_name.CREATED_AT,
        )

    def get_is_captain(self, obj: CrewMember) -> bool:
        return obj.is_captain()
