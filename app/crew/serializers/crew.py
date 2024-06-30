from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from crew.serializers.mixins import (
    MembersMixin,
    TagsMixin,
)
from crew.models import Crew
from crew.serializers.crew_activity import CrewActivitySerializer


class CrewSerializer(ModelSerializer, MembersMixin, TagsMixin):
    """크루에 대한 공개된 데이터를 다룬다."""

    members = SerializerMethodField()
    tags = SerializerMethodField()

    class Meta:
        model = Crew
        fields = [
            'emoji',
            'name',
            'members',
            'tags',
            'is_recruiting',
        ]


class CrewDetailSerializer(ModelSerializer, MembersMixin, TagsMixin):
    """크루에 대한 상세 데이터를 다룬다."""

    members = SerializerMethodField()
    tags = SerializerMethodField()
    activities = CrewActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = [
            'emoji',
            'name',
            'members',
            'tags',
            'activities',
            'is_active',
            'is_recruiting',
        ]
