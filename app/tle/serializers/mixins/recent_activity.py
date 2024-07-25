from datetime import date
from dataclasses import dataclass, asdict
from typing import Optional

from rest_framework.serializers import *

from tle.models import Crew, CrewActivity


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


class RecentActivityMixin:
    def recent_activity(self, crew: Crew) -> dict:
        if not crew.is_active:
            activity_dict = ActivityDict(name='활동 종료')
        elif (opened_activities := CrewActivity.opened_of_crew(crew)).exists():
            activity = opened_activities.earliest()
            activity_dict = ActivityDict.from_activity(activity)
        elif (closed_activities := CrewActivity.closed_of_crew(crew)).exists():
            activity = closed_activities.latest()
            activity_dict = ActivityDict.from_activity(activity)
        else:
            activity_dict = ActivityDict(name='등록된 활동 없음')
        return asdict(activity_dict)
