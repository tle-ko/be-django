from django.db.transaction import atomic
from rest_framework import serializers

from crews import enums
from crews import models
from crews import servicesa
from crews.serializersaaa import fields


PK = 'id'


class NoInputSerializer(serializers.Serializer):
    pass


# Crew Serializers

class CrewCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    custom_tags = serializers.ListField(
        default=list,
        child=serializers.CharField(),
    )
    languages = serializers.MultipleChoiceField(
        choices=enums.ProgrammingLanguageChoices.choices,
    )

    class Meta:
        model = models.Crew
        fields = [
            models.Crew.field_name.ICON,
            models.Crew.field_name.NAME,
            models.Crew.field_name.MAX_MEMBERS,
            'languages',
            models.Crew.field_name.MIN_BOJ_LEVEL,
            models.Crew.field_name.CUSTOM_TAGS,
            models.Crew.field_name.NOTICE,
            models.Crew.field_name.IS_RECRUITING,
            models.Crew.field_name.IS_ACTIVE,
            models.Crew.field_name.CREATED_BY,
        ]

    def save(self, **kwargs):
        languages = self.validated_data.pop('languages')
        with atomic():
            instance = super().save(**kwargs)
            service = servicesa.get_crew_service(instance)
            service.set_languages(languages)
        return instance


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
            models.Crew.field_name.IS_ACTIVE,
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
    is_captain = fields.IsCrewCaptainField()

    class Meta:
        model = models.Crew
        fields = [
            PK,
            models.Crew.field_name.ICON,
            models.Crew.field_name.NAME,
            models.Crew.field_name.NOTICE,
            'is_captain',
            'tags',
            'members',
            'activities',
        ]
        read_only_fields = ['__all__']


class CrewStatisticsSerializer(serializers.Serializer):
    difficulty = fields.ProblemStatisticsDifficultyField()
    tags = fields.ProblemStatisticsTagsField()


class CrewActivityDashboardSerializer(serializers.ModelSerializer):
    problems = fields.CrewAcitivityProblemsField()

    class Meta:
        model = models.CrewActivity
        fields = [
            PK,
            'problems',
        ]
        read_only_fields = ['__all__']


class CrewApplicationAboutApplicantSerializer(serializers.ModelSerializer):
    applicant = fields.CrewApplicationApplicantField()

    class Meta:
        model = models.CrewApplication
        fields = [
            PK,
            models.CrewApplication.field_name.MESSAGE,
            models.CrewApplication.field_name.IS_PENDING,
            models.CrewApplication.field_name.IS_ACCEPTED,
            models.CrewApplication.field_name.CREATED_AT,
            'applicant',
        ]
        read_only_fields = ['__all__']


class CrewApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CrewApplication


class CrewApplicationCreateSerializer(serializers.ModelSerializer):
    message = serializers.CharField()

    class Meta:
        model = models.CrewApplication
        fields = [
            models.CrewApplication.field_name.MESSAGE,
        ]
        read_only_fields = ['__all__']
