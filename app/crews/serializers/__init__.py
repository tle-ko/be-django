from rest_framework import serializers

from crews import models
from crews.serializers import fields


PK = 'id'


class RecruitingCrewSerializer(serializers.ModelSerializer):
    """크루 목록"""

    is_joinable = fields.CrewIsJoinableField()
    members = fields.CrewMemberCountField()
    tags = fields.CrewTagsField()
    latest_activity = fields.LatestActivityField()

    class Meta:
        model = models.Crew
        fields = [
            PK,
            models.Crew.field_name.ICON,
            models.Crew.field_name.NAME,
            models.Crew.field_name.IS_ACTIVE,
            'is_joinable',
            'members',
            'tags',
            'latest_activity',
        ]
        read_only_fields = ['__all__']


class MyCrewSerializer(serializers.ModelSerializer):
    "나의 참여 크루"

    latest_activity = fields.LatestActivityField()

    class Meta:
        model = models.Crew
        fields = [
            PK,
            models.Crew.field_name.ICON,
            models.Crew.field_name.NAME,
            'latest_activity',
        ]
        read_only_fields = ['__all__']


class CrewDashboardSerializer(serializers.ModelSerializer):
    """크루 대시보드

    -   공지사항
    -   크루 태그
    -   나의 동료
    -   크루가 풀이한 문제
    -   풀이한 문제의 난이도
    """

    tags = fields.CrewTagsField()
    members = fields.CrewMembersField()
    activities = fields.CrewActivitiesField()

    class Meta:
        model = models.Crew
        fields = [
            PK,
            models.Crew.field_name.ICON,
            models.Crew.field_name.NAME,
            models.Crew.field_name.NOTICE,
            'tags',
            'members',
            'activities',
        ]
        read_only_fields = ['__all__']


class CrewStatisticsSerializer(serializers.Serializer):
    difficulty = fields.ProblemStatisticsDifficultyField()
    tags = fields.ProblemStatisticsTagsField()


class MyCrewDashboardAcitivySerializer(serializers.ModelSerializer):
    problems = fields.CrewAcitivityProblemsField()

    class Meta:
        model = models.CrewActivity
        fields = [
            PK,
            'problems',
        ]
        read_only_fields = ['__all__']
