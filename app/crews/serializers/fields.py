from rest_framework import serializers

from crews import models
from crews import services
from crews import utils
from users.models import User


class LatestActivityField(serializers.SerializerMethodField):
    """마지막 활동회차"""

    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        if not crew.is_active:
            return {
                "name": "활동 종료",
                "date_start_at": None,
                "date_end_at": None,
            }
        queryset = services.crew_activities_queryset(crew)
        try:
            activity = queryset.latest()
        except models.CrewActivity.DoesNotExist:
            return {
                "name": "등록된 활동 없음",
                "date_start_at": None,
                "date_end_at": None,
            }
        else:
            return {
                "name": f"{queryset.count()}회차",
                "date_start_at": activity.start_at,
                "date_end_at": activity.end_at,
            }


class CrewMembersField(serializers.SerializerMethodField):
    """나의 동료"""

    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        queryset = models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.CREW: crew,
        })
        image_field = serializers.ImageField()
        return [
            {
                "username": member.user.username,
                "profile_image": image_field.to_representation(member.user.profile_image),
                "is_captain": member.is_captain,
            }
            for member in queryset
        ]


class CrewMemberCountField(serializers.SerializerMethodField):
    """크루 인원"""

    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        return {
            "count": services.crew_member_count(crew),
            "max_count": crew.max_members,
        }


class CrewTagsField(serializers.SerializerMethodField):
    """크루 태그"""

    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        return [
            {
                'key': tag.key,
                'name': tag.name,
                'type': tag.type.value,
            }
            for tag in services.crew_tags(crew)
        ]


class CrewIsJoinableField(serializers.SerializerMethodField):
    def to_representation(self, crew: models.Crew):
        user = serializers.CurrentUserDefault()(self)
        assert isinstance(crew, models.Crew)
        assert isinstance(user, User)
        return services.crew_is_joinable(crew, user)


class CrewIsMemberField(serializers.SerializerMethodField):
    def to_representation(self, crew: models.Crew):
        user = serializers.CurrentUserDefault()(self)
        assert isinstance(crew, models.Crew)
        assert isinstance(user, User)
        return services.crew_is_member(crew, user)


class CrewActivitiesField(serializers.SerializerMethodField):
    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        queryset = services.crew_activities_queryset(crew)
        return [
            {
                'id': activity.pk,
                'name': f'{n}회차',
            }
            for n, activity in enumerate(queryset, start=1)
        ]


class CrewAcitivityProblemsField(serializers.SerializerMethodField):
    def to_representation(self, activity: models.CrewActivity):
        assert isinstance(activity, models.CrewActivity)
        queryset = models.CrewActivityProblem.objects.filter(**{
            models.CrewActivityProblem.field_name.ACTIVITY: activity,
        })
        return [
            {
                'is_solved': problem,
            }
            for problem in queryset
        ]


class ProblemStatisticsField(serializers.SerializerMethodField):
    def to_representation(self, crew: models.Crew):
        statistics = services.problem_statistics(crew)
        return {
            'difficulty': [
                {
                    'difficulty': difficulty,
                    'problem_count': count,
                    'ratio': utils.divide_by_zero_handler(count, statistics.sample_count),
                }
                for difficulty, count in statistics.difficulty.items()
            ],
            'tags': [
                {
                    'label': {
                        'ko': tag.name_ko,
                        'en': tag.name_en,
                    },
                    'problem_count': count,
                    'ratio': utils.divide_by_zero_handler(count, statistics.sample_count),
                }
                for tag, count in statistics.tags.items()
            ],
        }
