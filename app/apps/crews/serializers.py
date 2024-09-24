from django.db.transaction import atomic
from rest_framework import serializers

from apps.activities.serializers import CrewActivityDTOSerializer

from users.serializers import UserDTOSerializer

from . import enums
from . import models
from . import proxy


PK = 'id'


class CrewMemberDTOSerializer(UserDTOSerializer):
    is_captain = serializers.BooleanField()


class CrewMemberCountDTOSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    max_count = serializers.IntegerField()


class CrewTagDTOSerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField()


class CrewDTOSerializer(serializers.Serializer):
    crew_id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.CharField()
    is_active = serializers.BooleanField()
    latest_activity = CrewActivityDTOSerializer()
    member_count = CrewMemberCountDTOSerializer()
    tags = CrewTagDTOSerializer(many=True)


class RecruitingCrewDTOSerializer(CrewDTOSerializer):
    is_appliable = serializers.BooleanField()


class CrewDetailDTOSerializer(CrewDTOSerializer):
    notice = serializers.CharField()
    members = CrewMemberDTOSerializer(many=True)
    activities = CrewActivityDTOSerializer(many=True)
    is_captain = serializers.BooleanField()


class CrewDAOSerializer(serializers.ModelSerializer):
    custom_tags = serializers.ListField(
        child=serializers.CharField(),
        default=list,
        write_only=True,
    )
    languages = serializers.MultipleChoiceField(
        choices=enums.ProgrammingLanguageChoices.choices,
        default=list,
        write_only=True,
    )
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.CrewDAO
        fields = [
            models.CrewDAO.field_name.ICON,
            models.CrewDAO.field_name.NAME,
            models.CrewDAO.field_name.MAX_MEMBERS,
            models.CrewDAO.field_name.MIN_BOJ_LEVEL,
            models.CrewDAO.field_name.NOTICE,
            models.CrewDAO.field_name.IS_RECRUITING,
            models.CrewDAO.field_name.IS_ACTIVE,
            models.CrewDAO.field_name.CREATED_BY,
            'custom_tags',
            'languages',
        ]

    @property
    def data(self):
        return proxy.Crew.as_dto(self.instance)

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data: dict) -> proxy.Crew:
        languages = validated_data.pop('languages')
        with atomic():
            instance = super().create(validated_data)
            proxy.Crew.set_submittable_languages(instance, languages)
        return instance

    def update(self, instance: models.CrewDAO, validated_data: dict) -> proxy.Crew:
        languages = validated_data.pop('languages')
        with atomic():
            instance = super().update(instance, validated_data)
            proxy.Crew.set_submittable_languages(instance, languages)
        return instance
