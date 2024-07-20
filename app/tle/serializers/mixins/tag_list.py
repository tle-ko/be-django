import dataclasses
import typing

from rest_framework.serializers import *

from tle.models import Crew
from tle.models.choices import BojUserLevel


@dataclasses.dataclass
class TagDict:
    key: str
    name: str


class TagListMixin:
    def tag_list(self, crew: Crew) -> typing.Dict:
        """크루의 태그들을 key와 name으로 나열하여 반환한다.

        반환 예시:

        ```python
        {
            "count": 2,
            "items": [
                { "key": "c", "name": "C" },
                { "key": None, "name": "티어 무관" }
            ]
        }
        ```
        """
        # 태그의 나열 순서는 리스트에 선언한 순서를 따름.
        tags: typing.List[TagDict] = [
            *self._get_language_tags(crew),
            *self._get_boj_level_tags(crew),
            *self._get_custom_tags(crew),
        ]
        return {
            'count': len(tags),
            'items': [dataclasses.asdict(tag) for tag in tags],
        }

    def _get_language_tags(self, crew: Crew) -> typing.Iterable[TagDict]:
        for lang in crew.submittable_languages.all():
            yield TagDict(key=lang.key, name=lang.name)

    def _get_boj_level_tags(self, crew: Crew) -> typing.Iterable[TagDict]:
        if crew.min_boj_level is not None:
            yield self._get_boj_level_bound_tag(crew.min_boj_level, 5, "이상")
        if crew.max_boj_level is not None:
            yield self._get_boj_level_bound_tag(crew.max_boj_level, 1, "이하")
        if crew.min_boj_level is None and crew.max_boj_level is None:
            yield TagDict(key=None, name="티어 무관")

    def _get_boj_level_bound_tag(self, level: int, bound_tier: int, bound_msg: str, lang='ko', arabic=False) -> TagDict:
        """level에 대한 백준 난이도 태그를 반환한다.

        bound_tier는 해당 랭크(브론즈,실버,...)를 모두 아우르는 마지막
        티어(1,2,3,4,5)를 의미한다.

        bound_msg는 "이상", 혹은 "이하"를 나타내는 제한 메시지이다.

        만약 level의 티어가 bound_tier와
        같다면 랭크만 출력하고,
        같지않다면 랭크와 티어 모두 출력한다.

        메시지의 마지막에는 bound_msg를 출력한다.
        """
        if BojUserLevel.get_tier(level) == bound_tier:
            level_name = BojUserLevel.get_division_name(level, lang=lang)
        else:
            level_name = BojUserLevel.get_name(level, lang=lang, arabic=arabic)
        return TagDict(key=None, name=f'{level_name} {bound_msg}')

    def _get_custom_tags(self, crew: Crew) -> typing.Iterable[TagDict]:
        for tag in crew.custom_tags:
            yield TagDict(key=None, name=tag)
