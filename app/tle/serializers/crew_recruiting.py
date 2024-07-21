from rest_framework.serializers import *

from tle.models import Crew
from tle.serializers.mixins import (
    CurrentUserMixin,
    TagListMixin,
    RecentActivityMixin,
)


class CrewRecruitingSerializer(CurrentUserMixin,
                               TagListMixin,
                               RecentActivityMixin,
                               ModelSerializer):
    is_joinable = SerializerMethodField()
    is_member = SerializerMethodField()
    activities = SerializerMethodField()
    members = SerializerMethodField()
    tags = SerializerMethodField()

    class Meta:
        model = Crew
        fields = [
            Crew.field_name.ICON,
            Crew.field_name.NAME,
            Crew.field_name.IS_RECRUITING,
            'is_joinable',
            'is_member',
            'activities',
            'members',
            'tags',
        ]
        read_only_fields = ['__all__']

    def get_is_joinable(self, obj: Crew):
        return obj.is_joinable(self.current_user())

    def get_is_member(self, obj: Crew):
        return obj.is_member(self.current_user())

    def get_activities(self, crew: Crew) -> dict:
        return {
            "count": crew.activities.count(),
            "recent": self.recent_activity(crew),
        }

    def get_members(self, obj: Crew):
        return {
            'count': obj.members.count(),
            'max_count': obj.max_members,
        }

    def get_tags(self, obj: Crew):
        return self.tag_list(obj)
