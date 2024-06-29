from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from boj.models import BOJLevel
from core.models import Language
from crew.models import Crew
from crew.serializers.crew_member import CrewMemberSerializer


class MembersMixin:
    def get_member_count(self, obj: Crew):
        return obj.members.count()

    def get_member_max_count(self, obj: Crew):
        return obj.max_member

    def get_members_list(self, obj: Crew):
        return CrewMemberSerializer(obj.members.all(), many=True).data

    def get_members(self, obj: Crew):
        return {
            'count': self.get_member_count(obj),
            'max_count': self.get_member_max_count(obj),
            'items': self.get_members_list(obj),
        }


class TagsMixin:
    def get_tags(self, obj: Crew):
        tags = []
        # Language tags
        for language in obj.languages.all():
            language: Language
            tags.append({
                'key': language.key,
                'name': language.name,
            })
        if obj.min_boj_tier is not None:
            tags.append({
                'key': None,
                'name': f'{BOJLevel(obj.min_boj_tier).label} 이상',
            })
        if obj.max_boj_tier is not None:
            tags.append({
                'key': None,
                'name': f'{BOJLevel(obj.max_boj_tier).label} 이하',
            })
        if obj.min_boj_tier is None and obj.max_boj_tier is None:
            tags.append({
                'key': None,
                'name': '티어 무관',
            })
        # Custom tags
        for tag in obj.tags:
            tags.append({
                'key': None,
                'name': tag,
            })
        return tags


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
