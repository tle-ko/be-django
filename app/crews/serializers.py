from typing import List
from typing import Union

from django.db.models import QuerySet
from django.db.transaction import atomic
from rest_framework import serializers

from crews.activities.models import CrewActivity
from crews.activities.serializers import CrewActivitySerializer
from crews.applications.services import is_valid_applicant
from crews.dto import CrewTagDTO
from crews.enums import ProgrammingLanguageChoices
from crews.models import Crew
from crews.models import CrewMember
from crews.models import CrewSubmittableLanguage
from users.models import User
from users.serializers import UserMinimalSerializer


PK = 'id'


# Crew Tag Serializer

class CrewTagTypeField(serializers.SerializerMethodField):
    def to_representation(self, value):
        return value

    def get_attribute(self, instance: CrewTagDTO) -> str:
        assert isinstance(instance, CrewTagDTO)
        return instance.type.value


class CrewTagSerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    type = CrewTagTypeField()


# Crew Member Serializer

class CrewMemberSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source=CrewMember.field_name.USER)
    username = serializers.CharField(
        source=CrewMember.field_name.USER+'__'+User.field_name.USERNAME,
    )
    profile_image = serializers.ImageField(
        source=CrewMember.field_name.USER+'__'+User.field_name.PROFILE_IMAGE,
    )

    class Meta:
        model = CrewMember
        fields = [
            'user_id',
            'username',
            'profile_image',
            CrewMember.field_name.IS_CAPTAIN,
        ]
        read_only_fields = ['__all__']


# Crew Fields

class IsJoinableField(serializers.SerializerMethodField):
    current_user = serializers.CurrentUserDefault()

    def to_representation(self, value):
        return value

    def get_attribute(self, instance: Crew):
        assert isinstance(instance, Crew)
        user: User = self.__class__.current_user(self)
        return user.is_authenticated and is_valid_applicant(instance, user, raise_exception=False)


class IsCaptainField(serializers.SerializerMethodField):
    current_user = serializers.CurrentUserDefault()

    def to_representation(self, value):
        return value

    def get_attribute(self, instance: Crew):
        assert isinstance(instance, Crew)
        user = self.__class__.current_user(self)
        return CrewMember.objects.filter(crew=instance, user=user, is_captain=True).exists()


class MemberField(serializers.SerializerMethodField):
    def __init__(self, include_member_details: bool, **kwargs):
        super().__init__(**kwargs)
        self.include_member_details = include_member_details

    def to_representation(self, crew: Crew):
        members = CrewMember.objects.filter(crew=crew)
        data = {
            "count": members.count(),
            "max_count": crew.max_members,
        }
        if self.include_member_details:
            data['items'] = CrewMemberSerializer(members, many=True).data
        return data

    def get_attribute(self, instance: Crew):
        assert isinstance(instance, Crew)
        return instance


class TagsField(serializers.ListSerializer):
    child = CrewTagSerializer()

    def to_representation(self, instance: Union[Crew, List[CrewTagDTO]]):
        if isinstance(instance, Crew):
            return super().to_representation(instance.tags())
        if isinstance(instance, list):
            return super().to_representation(instance)
        raise ValueError


class LatestActivityField(CrewActivitySerializer):
    def get_attribute(self, instance: Crew) -> CrewActivity:
        assert isinstance(instance, Crew)
        try:
            assert instance.is_active
            return CrewActivity.objects.crew(instance).has_started().latest()
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


class ActivitiesField(CrewActivitySerializer):
    def __init__(self, **kwargs):
        super().__init__(many=True, **kwargs)

    def get_attribute(self, instance: Crew) -> QuerySet[CrewActivity]:
        assert isinstance(instance, Crew)
        return CrewActivity.objects.crew(instance)


# Crew Serializers

class CrewCreateSerializer(serializers.ModelSerializer):
    created_by = UserMinimalSerializer()
    custom_tags = serializers.ListField(
        default=list,
        child=serializers.CharField(),
    )
    languages = serializers.MultipleChoiceField(
        choices=ProgrammingLanguageChoices.choices,
    )

    class Meta:
        model = Crew
        fields = [
            PK,
            Crew.field_name.ICON,
            Crew.field_name.NAME,
            Crew.field_name.MAX_MEMBERS,
            'languages',
            Crew.field_name.MIN_BOJ_LEVEL,
            Crew.field_name.NOTICE,
            Crew.field_name.IS_RECRUITING,
            Crew.field_name.IS_ACTIVE,
            Crew.field_name.CREATED_AT,
            Crew.field_name.CREATED_BY,
            Crew.field_name.CUSTOM_TAGS,
        ]
        extra_kwargs = {
            PK: {
                'read_only': True,
            },
            'languages': {
                'write_only': True,
                'default': list,
            },
            Crew.field_name.CREATED_AT: {
                'read_only': True,
            },
            Crew.field_name.CREATED_BY: {
                'read_only': True,
                'default': serializers.CurrentUserDefault(),
            },
        }

    def save(self, **kwargs):
        languages = self.validated_data.pop('languages')
        with atomic():
            crew = super().save(**kwargs)
            CrewSubmittableLanguage.objects.crew(crew).delete()
            CrewSubmittableLanguage.objects.bulk_create_from_languages(
                crew=crew,
                languages=languages,
            )
        return crew


class RecruitingCrewSerializer(serializers.ModelSerializer):
    """크루 목록"""
    is_joinable = IsJoinableField()
    members = MemberField(include_member_details=False)
    tags = TagsField()
    latest_activity = LatestActivityField()

    class Meta:
        model = Crew
        fields = [
            PK,
            Crew.field_name.ICON,
            Crew.field_name.NAME,
            Crew.field_name.IS_ACTIVE,
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
        model = Crew
        fields = [
            PK,
            Crew.field_name.ICON,
            Crew.field_name.NAME,
            Crew.field_name.IS_ACTIVE,
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
    activities = CrewActivitySerializer()
    is_captain = IsCaptainField()

    class Meta:
        model = Crew
        fields = [
            PK,
            Crew.field_name.ICON,
            Crew.field_name.NAME,
            Crew.field_name.NOTICE,
            'is_captain',
            'tags',
            'members',
            'activities',
        ]
        read_only_fields = ['__all__']
