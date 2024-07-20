from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional

from rest_framework.serializers import *

from tle.models import Crew, CrewActivity


@dataclass
class ActivityDict:
    name: str
    nth: Optional[int] = None
    in_progress: bool = False
    start_at: Optional[date] = None
    end_at: Optional[date] = None


class CrewJoinedSerializer(ModelSerializer):
    activities = SerializerMethodField()

    class Meta:
        model = Crew
        fields = [
            Crew.field_name.EMOJI,
            Crew.field_name.NAME,
            'activities',
            Crew.field_name.IS_ACTIVE,
        ]
        read_only_fields = ['__all__']

    def get_activities(self, crew: Crew) -> dict:
        return {
            "count": crew.activities.count(),
            "recent": self.get_recent_activity(crew),
        }

    def get_recent_activity(self, crew: Crew) -> dict:
        if not crew.is_active:
            activity_dict = ActivityDict(
                name='활동 종료',
            )
        elif (opened_activities := CrewActivity.opened_of_crew(crew)).exists():
            activity = opened_activities.earliest()
            activity_dict = ActivityDict(
                name=activity.name,
                nth=activity.nth(),
                start_at=activity.start_at.date(),
                end_at=activity.end_at.date(),
                in_progress=activity.is_open(),
            )
        elif (closed_activities := CrewActivity.closed_of_crew(crew)).exists():
            activity = closed_activities.latest()
            activity_dict = ActivityDict(
                nth=activity.nth(),
                name=activity.name,
                start_at=activity.start_at.date(),
                end_at=activity.end_at.date(),
                in_progress=activity.is_open(),
            )
        else:
            activity_dict = ActivityDict(
                name='등록된 활동 없음',
            )
        return asdict(activity_dict)
