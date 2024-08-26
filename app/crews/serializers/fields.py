from rest_framework import serializers

from boj.services import get_boj_user_service
from crews import dto
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
        try:
            service = services.CrewActivityService.last_started(crew)
        except models.CrewActivity.DoesNotExist:
            return {
                "name": "등록된 활동 없음",
                "date_start_at": None,
                "date_end_at": None,
            }
        else:
            return {
                "name": f"{service.nth()}회차",
                "date_start_at": service.instance.start_at,
                "date_end_at": service.instance.end_at,
            }


class IsCrewCaptainField(serializers.SerializerMethodField):
    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        user = serializers.CurrentUserDefault()(self)
        service = services.CrewService(crew)
        return service.is_captain(user)


class CrewMembersField(serializers.SerializerMethodField):
    """나의 동료"""

    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        service = services.CrewService(crew)
        image_field = serializers.ImageField()
        return [
            {
                "username": member.user.username,
                "profile_image": image_field.to_representation(member.user.profile_image),
                "is_captain": member.is_captain,
            }
            for member in service.query_members()
        ]


class CrewMemberCountField(serializers.SerializerMethodField):
    """크루 인원"""

    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        service = services.CrewService(crew)
        return {
            "count": service.query_members().count(),
            "max_count": crew.max_members,
        }


class CrewTagsField(serializers.SerializerMethodField):
    """크루 태그"""

    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        service = services.CrewService(crew)
        return [
            {
                'key': tag.key,
                'name': tag.name,
                'type': tag.type.value,
            }
            for tag in service.tags()
        ]


class CrewIsJoinableField(serializers.SerializerMethodField):
    def to_representation(self, crew: models.Crew):
        user = serializers.CurrentUserDefault()(self)
        assert isinstance(crew, models.Crew)
        assert isinstance(user, User)
        service = services.CrewService(crew)
        return service.validate_applicant(user)


class CrewIsMemberField(serializers.SerializerMethodField):
    def to_representation(self, crew: models.Crew):
        user = serializers.CurrentUserDefault()(self)
        assert isinstance(crew, models.Crew)
        assert isinstance(user, User)
        service = services.CrewService(crew)
        return service.is_member(user)


class CrewActivitiesField(serializers.SerializerMethodField):
    def to_representation(self, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        service = services.CrewService(crew)
        return [
            {
                'activity_id': activity.activity_id,
                'name': activity.name,
            }
            for activity in service.activities()
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


class ProblemStatisticsDifficultyField(serializers.SerializerMethodField):
    def to_representation(self, statistics: dto.ProblemStatistic):
        assert isinstance(statistics, dto.ProblemStatistic)
        return [
            {
                'difficulty': difficulty,
                'problem_count': count,
                'ratio': utils.divide_by_zero_handler(count, statistics.sample_count),
            }
            for difficulty, count in statistics.difficulty.items()
        ]


class ProblemStatisticsTagsField(serializers.SerializerMethodField):
    def to_representation(self, statistics: dto.ProblemStatistic):
        assert isinstance(statistics, dto.ProblemStatistic)
        return [
            {
                'label': {
                    'ko': tag.name_ko,
                    'en': tag.name_en,
                },
                'problem_count': count,
                'ratio': utils.divide_by_zero_handler(count, statistics.sample_count),
            }
            for tag, count in statistics.tags.items()
        ]


class CrewApplicationApplicantField(serializers.SerializerMethodField):
    def to_representation(self, instance: models.CrewApplication):
        assert isinstance(instance, models.CrewApplication)
        service = get_boj_user_service(instance.applicant.boj_username)
        level = service.level()
        return {
            "user_id": instance.applicant.pk,
            "username": instance.applicant.username,
            "profile_image": instance.applicant.profile_image.url,
            "boj": {
                "level": {
                    "value": level.value,
                    "name": level.get_name(lang="ko", arabic=False),
                }
            }
        }
