from dataclasses import asdict, dataclass
from datetime import date
from enum import Enum
from typing import Iterable, List, Optional

from rest_framework.serializers import ReadOnlyField

from crews.models import Crew, CrewActivity
from crews.serializers.mixins import CurrentUserMixin
from crews.services import get_members, is_member, is_joinable
from users.models import UserBojLevelChoices


class MemberCountField(ReadOnlyField):
    def to_representation(self, crew: Crew):
        members = get_members(crew)
        return {
            'count': members.count(),
            'max_count': crew.max_members,
        }


class MembersField(ReadOnlyField):
    def to_representation(self, crew: Crew):
        members = get_members(crew)
        return {
            'count': members.count(),
            'max_count': crew.max_members,
            'items': [{
                "user_id": member.user.pk,
                "username": member.user.username,
                "profile_image": member.user.profile_image,
                "is_captain": member.is_captain,
                "created_at": member.created_at,
            } for member in members],
        }


class IsMemberField(CurrentUserMixin,
                    ReadOnlyField):
    def to_representation(self, crew: Crew):
        user = self.current_user()
        return is_member(crew, user)


class IsJoinableField(CurrentUserMixin,
                      ReadOnlyField):
    def to_representation(self, crew: Crew):
        user = self.current_user()
        return is_joinable(crew, user)


class TagType(Enum):
    LANGUAGE = 'language'
    LEVEL = 'level'
    CUSTOM = 'custom'


@dataclass
class TagDict:
    key: str
    name: str
    type: TagType


class TagsField(ReadOnlyField):
    def to_representation(self, crew: Crew):
        # 태그의 나열 순서는 리스트에 선언한 순서를 따름.
        tags: List[TagDict] = [
            *self.get_language_tags(crew),
            *self.get_level_tags(crew),
            *self.get_custom_tags(crew),
        ]
        return {
            'count': len(tags),
            'items': [asdict(tag) for tag in tags],
        }

    def get_custom_tags(self, crew: Crew) -> Iterable[TagDict]:
        for tag in crew.custom_tags:
            yield TagDict(
                key=None,
                name=tag,
                type=TagType.CUSTOM.value,
            )

    def get_language_tags(self, crew: Crew) -> Iterable[TagDict]:
        for lang in crew.submittable_languages.all():
            yield TagDict(
                key=lang.key,
                name=lang.name,
                type=TagType.LANGUAGE.value,
            )

    def get_level_tags(self, crew: Crew) -> Iterable[TagDict]:
        yield TagDict(
            key=None,
            name=self.get_boj_level_bounded_name(
                level=UserBojLevelChoices(crew.min_boj_level),
            ),
            type=TagType.LEVEL.value,
        )

    def get_boj_level_bounded_name(self,
                                   level: Optional[UserBojLevelChoices],
                                   bound_tier: int = 5,
                                   bound_msg: str = "이상",
                                   default_msg: str = "티어 무관",
                                   lang='ko',
                                   arabic=False) -> str:
        """level에 대한 백준 난이도 태그 이름을 반환한다.

        bound_tier는 해당 랭크(브론즈,실버,...)를 모두 아우르는 마지막
        티어(1,2,3,4,5)를 의미한다.

        bound_msg는 "이상", 혹은 "이하"를 나타내는 제한 메시지이다.

        만약 level의 티어가 bound_tier와
        같다면 랭크만 출력하고,
        같지않다면 랭크와 티어 모두 출력한다.

        메시지의 마지막에는 bound_msg를 출력한다.
        """
        if level is None:
            return default_msg
        if level.get_tier() == bound_tier:
            return level.get_division_name(lang=lang) + ' ' + bound_msg
        else:
            return level.get_name(lang=lang, arabic=arabic) + ' ' + bound_msg


@dataclass
class ActivityDict:
    nth: Optional[int] = None
    name: str = ''
    start_at: Optional[date] = None
    end_at: Optional[date] = None
    is_open: bool = False  # 제출 가능 여부

    @classmethod
    def from_activity(cls, activity: CrewActivity) -> 'ActivityDict':
        return ActivityDict(
            name=activity.name,
            nth=activity.nth(),
            is_open=activity.is_opened(),
            start_at=activity.start_at,
            end_at=activity.end_at,
        )


class RecentActivityField(ReadOnlyField):
    def to_representation(self, crew: Crew):
        activities = CrewActivity.objects.filter(**{
            CrewActivity.field_name.CREW: crew,
        })
        return {
            'count': activities.count(),
            "recent": asdict(self.get_recent_activity(crew)),
        }

    def get_recent_activity(self, crew: Crew) -> ActivityDict:
        # 활동 종료 여부가 최우선 순위
        if not crew.is_active:
            return ActivityDict(name='활동 종료')
        # 활동 중이라면, 현재 진행 중인 활동 중 가장 오래된 것을 우선적으로 표시
        if (opened_activities := CrewActivity.opened_of_crew(crew)).exists():
            activity = opened_activities.earliest()
            return ActivityDict.from_activity(activity)
        # 현재 진행 중인 활동이 없다면, 가장 최근 활동을 표시
        if (closed_activities := CrewActivity.closed_of_crew(crew)).exists():
            activity = closed_activities.latest()
            return ActivityDict.from_activity(activity)
        # 활동 중이나, 등록된 활동이 없다면 '등록된 활동 없음'을 표시
        return ActivityDict(name='등록된 활동 없음')
