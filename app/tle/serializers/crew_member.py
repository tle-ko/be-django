from rest_framework.serializers import *

from tle.models import CrewMember
from tle.serializers.user_minimal import UserMinimalSerializer


class CrewMemberSerializer(ModelSerializer):
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = CrewMember
        fields = (
            CrewMember.field_name.USER,
            CrewMember.field_name.IS_CAPTAIN,
            CrewMember.field_name.CREATED_AT,
        )
        read_only_fields = '__all__'
