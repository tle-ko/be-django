from rest_framework.serializers import *

from tle.models import Crew
from tle.serializers.mixins import CurrentUserMixin


class CrewRecruitingSerializer(ModelSerializer, CurrentUserMixin):
    is_joinable = SerializerMethodField()
    is_member = SerializerMethodField()
    members = SerializerMethodField()
    tags = SerializerMethodField()

    class Meta:
        model = Crew
        fields = [
            Crew.field_name.NAME,
            Crew.field_name.EMOJI,
            Crew.field_name.IS_RECRUITING,
            'is_joinable',
            'is_member',
            'members',
            'tags',
        ]
        read_only_fields = ['__all__']

    def get_is_joinable(self, obj: Crew):
        return obj.is_recruiting

    def get_is_member(self, obj: Crew):
        return obj.members.filter(user=self.current_user()).exists()

    def get_members(self, obj: Crew):
        return {
            'count': obj.members.count(),
            'max_count': obj.max_members,
        }

    def get_tags(self, obj: Crew):
        tags = obj.get_tags()
        return {
            'count': len(tags),
            'items': [{'key': tag.key, 'name': tag.name} for tag in tags],
        }
