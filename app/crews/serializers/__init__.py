from rest_framework import serializers

from crews import enums
from crews import models
from crews import services
from crews.serializers import fields
from users.serializers import UserMinimalSerializer


PK = 'id'


class NoInputSerializer(serializers.Serializer):
    pass


class CrewCreateSerializer(serializers.ModelSerializer):
    languages = serializers.MultipleChoiceField(choices=enums.ProgrammingLanguageChoices.choices)

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
        ]
        extra_kwargs = {
            models.Crew.field_name.CUSTOM_TAGS: {
                'default': list,
            }
        }

    def save(self, **kwargs):
        return services.CrewService.create(**self.validated_data)


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


class CrewApplicationCreateSerializer(serializers.Serializer):
    message = serializers.CharField()
