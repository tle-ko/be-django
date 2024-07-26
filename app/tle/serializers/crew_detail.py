from django.db.models import QuerySet
from django.db.transaction import atomic
from rest_framework.serializers import *

from users.serializers import UserMinimalSerializer
from tle.models import Crew, SubmissionLanguage
from tle.serializers.crew_member import CrewMemberSerializer
from tle.serializers.mixins import CurrentUserMixin, TagListMixin


class CrewDetailSerializer(ModelSerializer, CurrentUserMixin, TagListMixin):
    is_member = SerializerMethodField()
    members = SerializerMethodField()
    languages = JSONField(help_text='사용 가능한 언어 목록 (언어 key의 배열)')
    tags = SerializerMethodField()
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
            Crew.field_name.MIN_BOJ_LEVEL,
            'languages',
            Crew.field_name.CUSTOM_TAGS,
            'tags',
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

    def create(self, validated_data):
        return super().create(validated_data)

    def get_is_member(self, obj: Crew):
        return obj.is_member(self.current_user())

    def get_members(self, obj: Crew):
        return {
            'count': obj.members.count(),
            'max_count': obj.max_members,
            'items': CrewMemberSerializer(obj.members.all(), many=True).data,
        }

    def get_tags(self, obj: Crew):
        return self.tag_list(obj)

    def validate_languages(self, value) -> QuerySet[SubmissionLanguage]:
        """언어 정보를 언어 키의 배열로 받고, 이를 SubmissionLanguage의 QuerySet으로 변환한다."""
        # 언어 정보는 문자열의 배열로 받는다.
        if not isinstance(value, list):
            raise ValidationError('Languages must be a list of strings')
        for lang in value:
            if not isinstance(lang, str):
                raise ValidationError('Languages must be a list of strings')
        # 최소 한 개 이상의 언어가 있어야 한다.
        if len(value) == 0:
            raise ValidationError('At least one language must be specified')
        for lang in value:
            if not SubmissionLanguage.objects.filter(**{
                SubmissionLanguage.field_name.KEY: lang,
            }).exists():
                raise ValidationError(f'Invalid language key "{lang}"')
        # 언어 키의 배열을 SubmissionLanguage의 QuerySet으로 변환한다.
        return SubmissionLanguage.objects.filter(**{
            SubmissionLanguage.field_name.KEY + '__in': value,
        })

    def save(self, **kwargs):
        crew: Crew
        languages: QuerySet[SubmissionLanguage]
        languages = self.validated_data.pop('languages')
        with atomic():
            crew = super().save(**{
                **kwargs,
                Crew.field_name.CREATED_BY: self.current_user(),
            })
            crew.submittable_languages.set(languages)
            crew.save()
        return crew