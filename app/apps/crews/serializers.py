from typing import List
from typing import Union

from django.db.models import QuerySet
from django.db.transaction import atomic
from rest_framework import serializers

from apps.activities.serializers import CrewActivityDTOSerializer
from apps.activities.models import CrewActivity
from apps.applications.services import is_valid_applicant

from users.models import User
from users.serializers import UserDTOSerializer
from users.serializers import UserMinimalSerializer

from . import dto
from . import enums
from . import models


PK = 'id'


class CrewMemberDTOSerializer(UserDTOSerializer):
    is_captain = serializers.BooleanField()


class CrewDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='pk')
    crew_id = serializers.IntegerField(source='pk')
    is_active = serializers.BooleanField()
    name = serializers.CharField()
    icon = serializers.CharField()
    latest_activity = CrewActivityDTOSerializer()


class CrewTagDTOSerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField()


class CrewDashboardDTOSerializer(CrewDTOSerializer):
    is_captain = serializers.BooleanField()
    notice = serializers.CharField()
    tags = CrewTagDTOSerializer(many=True)
    members = CrewMemberDTOSerializer(many=True)
    activities = CrewActivityDTOSerializer(many=True)


class CrewTagTypeField(serializers.SerializerMethodField):
    def to_representation(self, value):
        return value

    def get_attribute(self, instance: dto.CrewTagDTO) -> str:
        assert isinstance(instance, dto.CrewTagDTO)
        return instance.type.value


class CrewTagSerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    type = CrewTagTypeField()


# Crew Member Serializer

class CrewMemberSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source=models.CrewMember.field_name.USER)
    username = serializers.CharField(
        source=models.CrewMember.field_name.USER+'__'+User.field_name.USERNAME,
    )
    profile_image = serializers.ImageField(
        source=models.CrewMember.field_name.USER+'__'+User.field_name.PROFILE_IMAGE,
    )

    class Meta:
        model = models.CrewMember
        fields = [
            'user_id',
            'username',
            'profile_image',
            models.CrewMember.field_name.IS_CAPTAIN,
        ]
        read_only_fields = ['__all__']


# Crew Fields

class IsJoinableField(serializers.SerializerMethodField):
    current_user = serializers.CurrentUserDefault()

    def to_representation(self, value):
        return value

    def get_attribute(self, instance: models.Crew):
        assert isinstance(instance, models.Crew)
        user: User = self.__class__.current_user(self)
        return user.is_authenticated and is_valid_applicant(instance, user, raise_exception=False)


class IsCaptainField(serializers.SerializerMethodField):
    current_user = serializers.CurrentUserDefault()

    def to_representation(self, value):
        return value

    def get_attribute(self, instance: models.Crew):
        assert isinstance(instance, models.Crew)
        user = self.__class__.current_user(self)
        return models.CrewMember.objects.filter(crew=instance, user=user, is_captain=True).exists()


class MemberField(serializers.SerializerMethodField):
    def __init__(self, include_member_details: bool, **kwargs):
        super().__init__(**kwargs)
        self.include_member_details = include_member_details

    def to_representation(self, crew: models.Crew):
        members = models.CrewMember.objects.filter(
            crew=crew).select_related(models.CrewMember.field_name.USER)
        users = [member.user for member in members]
        data = {
            "count": len(users),
            "max_count": crew.max_members,
        }
        if self.include_member_details:
            data['items'] = UserMinimalSerializer(users, many=True).data
        return data

    def get_attribute(self, instance: models.Crew):
        assert isinstance(instance, models.Crew)
        return instance


class TagsField(serializers.ListSerializer):
    child = CrewTagSerializer()

    def to_representation(self, instance: Union[models.Crew, List[dto.CrewTagDTO]]):
        if isinstance(instance, models.Crew):
            return super().to_representation(instance.tags())
        if isinstance(instance, list):
            return super().to_representation(instance)
        raise ValueError


class LatestActivityField(serializers.SerializerMethodField):
    def get_attribute(self, instance: models.Crew) -> CrewActivity:
        assert isinstance(instance, models.Crew)
        try:
            assert instance.is_active
            return CrewActivity.objects.filter(crew=instance, has_started=True).latest()
        except CrewActivity.DoesNotExist:
            return CrewActivity(**{
                CrewActivity.field_name.CREW: instance,
                CrewActivity.field_name.NAME: '등록된 활동 없음',
                CrewActivity.field_name.START_AT: None,
                CrewActivity.field_name.END_AT: None,
            })
        except AssertionError:
            return CrewActivity(**{
                CrewActivity.field_name.CREW: instance,
                CrewActivity.field_name.NAME: '활동 종료',
                CrewActivity.field_name.START_AT: None,
                CrewActivity.field_name.END_AT: None,
            })


class ActivitiesField(serializers.SerializerMethodField):
    def to_representation(self, queryset: QuerySet[CrewActivity]):
        # return serializers.SerializerMethodField(queryset, many=True).data
        return {}

    def get_attribute(self, instance: models.Crew) -> QuerySet[CrewActivity]:
        assert isinstance(instance, models.Crew)
        return CrewActivity.objects.filter(crew=instance)


# Crew Serializers

class CrewCreateSerializer(serializers.ModelSerializer):
    created_by = UserMinimalSerializer(read_only=True)
    custom_tags = serializers.ListField(
        default=list,
        child=serializers.CharField(),
    )
    languages = serializers.MultipleChoiceField(
        choices=enums.ProgrammingLanguageChoices.choices,
        default=list,
        write_only=True,
    )

    class Meta:
        model = models.Crew
        fields = [
            PK,
            models.Crew.field_name.ICON,
            models.Crew.field_name.NAME,
            models.Crew.field_name.MAX_MEMBERS,
            'languages',
            models.Crew.field_name.MIN_BOJ_LEVEL,
            models.Crew.field_name.NOTICE,
            models.Crew.field_name.IS_RECRUITING,
            models.Crew.field_name.IS_ACTIVE,
            models.Crew.field_name.CREATED_AT,
            models.Crew.field_name.CREATED_BY,
            models.Crew.field_name.CUSTOM_TAGS,
        ]
        extra_kwargs = {
            PK: {'read_only': True},
            models.Crew.field_name.CREATED_AT: {'read_only': True},
        }

    def save(self, **kwargs):
        languages = self.validated_data.pop('languages')
        with atomic():
            self.instance = models.Crew.objects.create(**{
                models.Crew.field_name.CREATED_BY: serializers.CurrentUserDefault()(self),
                **self.validated_data,
                **kwargs,
            })
            models.CrewSubmittableLanguage.objects.filter(crew=self.instance).delete()
            models.CrewSubmittableLanguage.objects.bulk_create_from_languages(
                crew=self.instance,
                languages=languages,
            )
        return self.instance


class RecruitingCrewSerializer(serializers.ModelSerializer):
    """크루 목록"""
    is_joinable = IsJoinableField()
    members = MemberField(include_member_details=False)
    tags = TagsField()
    latest_activity = LatestActivityField()

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
    latest_activity = LatestActivityField()

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

    tags = TagsField()
    members = MemberField(include_member_details=True)
    activities = ActivitiesField()
    is_captain = IsCaptainField()

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
