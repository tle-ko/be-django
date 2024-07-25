from rest_framework.serializers import *

from tle.models import Crew
from tle.serializers.mixins import RecentActivityMixin


class CrewJoinedSerializer(ModelSerializer, RecentActivityMixin):
    activities = SerializerMethodField()

    class Meta:
        model = Crew
        fields = [
            Crew.field_name.ICON,
            Crew.field_name.NAME,
            'activities',
            Crew.field_name.IS_ACTIVE,
        ]
        read_only_fields = ['__all__']

    def get_activities(self, crew: Crew) -> dict:
        return {
            "count": crew.activities.count(),
            "recent": self.recent_activity(crew),
        }
