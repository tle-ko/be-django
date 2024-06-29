from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from crew.serializers.mixins import (
    MembersMixin,
    TagsMixin,
)
from crew.models import Crew


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
