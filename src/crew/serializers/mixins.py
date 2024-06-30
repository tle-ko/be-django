from typing import (
    Iterable,
)

from boj.models import BOJLevel
from core.models import Language
from crew.models import Crew
from crew.serializers.crew_member import CrewMemberSerializer


class MembersMixin:
    def get_members(self, obj: Crew):
        return {
            'count': self._get_member_count(obj),
            'max_count': self._get_member_max_count(obj),
            'items': self._get_members_list(obj),
        }

    def _get_member_count(self, obj: Crew):
        return obj.members.count()

    def _get_member_max_count(self, obj: Crew):
        return obj.max_member

    def _get_members_list(self, obj: Crew):
        return CrewMemberSerializer(obj.members.all(), many=True).data


class TagsMixin:
    def get_tags(self, obj: Crew):
        tags = [
            *self._get_language_tags(obj),
            *self._get_tier_tags(obj),
            *self._get_custom_tags(obj),
        ]
        return {
            'count': len(tags),
            'items': tags,
        }

    def _get_language_tags(self, obj: Crew):
        languages: Iterable[Language] = obj.languages.all()
        return [{'key': lang.key, 'name': lang.name} for lang in languages]

    def _get_tier_tags(self, obj: Crew):
        tags = []
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
        return tags

    def _get_custom_tags(self, obj: Crew):
        return [{'key': None, 'name': tag} for tag in obj.tags]
