from django.db.transaction import atomic
from rest_framework.serializers import (
    ModelSerializer,
    MultipleChoiceField,
)

from crews.models import (
    Crew,
    CrewSubmittableLanguage,
    ProgrammingLanguageChoices,
)
from crews.serializers.fields import (
    MembersField,
    MemberCountField,
    IsMemberField,
    IsJoinableField,
    TagsField,
    RecentActivityField,
)
from crews.serializers.mixins import (
    CurrentUserMixin,
    ReadOnlySerializerMixin,
)
from crews.services import set_crew_submittable_languages
from users.serializers import UserMinimalSerializer


class CrewDetailSerializer(CurrentUserMixin,
                           ModelSerializer):
    is_member = IsMemberField()
    members = MemberCountField()
    tags = TagsField()
    languages = MultipleChoiceField(choices=ProgrammingLanguageChoices.choices)
    created_by = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Crew
        fields = [
            'id',
            Crew.field_name.ICON,
            Crew.field_name.NAME,
            Crew.field_name.MAX_MEMBERS,
            'members',
            'is_member',
            'languages',
            'tags',
            Crew.field_name.MIN_BOJ_LEVEL,
            Crew.field_name.CUSTOM_TAGS,
            Crew.field_name.NOTICE,
            Crew.field_name.IS_RECRUITING,
            Crew.field_name.IS_ACTIVE,
            Crew.field_name.CREATED_AT,
            Crew.field_name.CREATED_BY,
            Crew.field_name.UPDATED_AT,
        ]
        read_only_fields = [
            'id',
            'tags',
            'members',
            Crew.field_name.CREATED_AT,
            Crew.field_name.CREATED_BY,
            Crew.field_name.UPDATED_AT,
        ]
        extra_kwargs = {
            Crew.field_name.MAX_MEMBERS: {'write_only': True},
            Crew.field_name.MIN_BOJ_LEVEL: {'write_only': True},
            'languages': {'write_only': True},
            Crew.field_name.CUSTOM_TAGS: {'write_only': True},
        }

    def save(self, **kwargs):
        languages = self.validated_data.pop('languages')
        with atomic():
            crew: Crew = super().save(**kwargs)
            set_crew_submittable_languages(crew, languages)
        return crew

    def create(self, validated_data):
        validated_data[Crew.field_name.CREATED_BY] = self.current_user()
        return super().create(validated_data)


class CrewRecruitingSerializer(ReadOnlySerializerMixin,
                               ModelSerializer):
    is_joinable = IsJoinableField()
    is_member = IsMemberField()
    activities = RecentActivityField()
    members = MembersField()
    tags = TagsField()

    class Meta:
        model = Crew
        fields = [
            Crew.field_name.ICON,
            Crew.field_name.NAME,
            Crew.field_name.IS_ACTIVE,
            Crew.field_name.IS_RECRUITING,
            'is_joinable',
            'is_member',
            'activities',
            'members',
            'tags',
        ]
        read_only_fields = ['__all__']


class CrewJoinedSerializer(ReadOnlySerializerMixin,
                           ModelSerializer):
    activities = RecentActivityField()

    class Meta:
        model = Crew
        fields = [
            Crew.field_name.ICON,
            Crew.field_name.NAME,
            Crew.field_name.IS_ACTIVE,
            'activities',
        ]
        read_only_fields = ['__all__']
