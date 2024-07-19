import typing

from rest_framework.serializers import *

from tle.models import Crew, User, UserSolvedTier


class CrewRecruitingSerializer(ModelSerializer):
    members = SerializerMethodField()
    tags = SerializerMethodField()
    is_joinable = SerializerMethodField()

    class Meta:
        model = Crew
        fields = [
            'name',
            'emoji',
            'members',
            'tags',
            'is_joinable',
        ]

    def get_members(self, obj: Crew):
        return {
            'count': obj.members.count(),
            'max_count': obj.max_members,
        }

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

    def get_is_joinable(self, obj: Crew):
        user = self._get_user()
        assert user.is_authenticated
        return obj.is_joinable(user)

    def _get_user(self) -> User:
        return self.context['request'].user

    def _get_language_tags(self, obj: Crew):
        return [
            self._tag_item(lang.key, lang.name)
            for lang in obj.submittable_languages.all()
        ]

    def _get_tier_tags(self, obj: Crew):
        tags = []
        if obj.min_boj_tier is not None:
            name = f'{UserSolvedTier(obj.min_boj_tier).label} 이상'
            tags.append(self._tag_item(None, name))
        if obj.max_boj_tier is not None:
            name = f'{UserSolvedTier(obj.max_boj_tier).label} 이하'
            tags.append(self._tag_item(None, name))
        if obj.min_boj_tier is None and obj.max_boj_tier is None:
            name = f'티어 무관'
            tags.append(self._tag_item(None, name))
        return tags

    def _get_custom_tags(self, obj: Crew):
        return [self._tag_item(None, tag) for tag in obj.custom_tags]

    def _tag_item(self, key: typing.Optional[str], name: str):
        return {
            'key': key,
            'name': name,
        }
