from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from crew.models import CrewMember


class CrewMemberSerializer(ModelSerializer):
    is_host = SerializerMethodField()

    class Meta:
        model = CrewMember
        fields = (
            'user',
            'is_host',
        )

    def get_is_host(self, obj: CrewMember) -> bool:
        return obj.crew.captain == obj.user
