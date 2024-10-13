import typing

from django.db.transaction import atomic
from rest_framework import serializers

from apps.boj.serializers import BOJUserDTOSerializer
from apps.problems.serializers import ProblemDTOSerializer
from apps.problems.serializers import ProblemDetailDTOSerializer
from apps.problems.serializers import ProblemStatisticDTOSerializer
from apps.submissions.serializers import SubmissionDTOSerializer
from common.serializers import GenericModelToDTOSerializer
from users.serializers import UserDTOSerializer

from . import converters
from . import enums
from . import models


class EmptySerializer(serializers.Serializer):
    pass


class CrewActivityProblemDTOSerializer(ProblemDTOSerializer):
    problem_id = serializers.IntegerField()
    order = serializers.IntegerField()
    submission_id = serializers.IntegerField()
    has_submitted = serializers.BooleanField()
    submissions = SubmissionDTOSerializer(many=True)


class CrewActivityProblemDetailDTOSerializer(ProblemDetailDTOSerializer):
    problem_id = serializers.IntegerField()
    order = serializers.IntegerField()
    submission_id = serializers.IntegerField()
    has_submitted = serializers.BooleanField()


class CrewActivityDTOSerializer(serializers.Serializer):
    activity_id = serializers.IntegerField()
    name = serializers.CharField()
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    is_in_progress = serializers.BooleanField()
    has_started = serializers.BooleanField()
    has_ended = serializers.BooleanField()


class CrewActivityDetailDTOSerializer(CrewActivityDTOSerializer):
    problems = CrewActivityProblemDTOSerializer(many=True)


class CrewActivityDAOSerializer(GenericModelToDTOSerializer):
    model_converter_class = converters.CrewActivityDetailConverter
    dto_serializer_class = CrewActivityDetailDTOSerializer

    problem_refs = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = models.CrewActivityDAO
        fields = [
            models.CrewActivityDAO.field_name.START_AT,
            models.CrewActivityDAO.field_name.END_AT,
            'problem_refs',
        ]

    def save(self, **kwargs):
        problem_ref_ids: typing.List[int]
        problem_ref_ids = self.validated_data.pop('problem_refs')
        problem_refs = models.ProblemDAO.objects.filter(pk__in=problem_ref_ids)
        with atomic():
            instance: models.CrewActivityDAO = super().save(**kwargs)
            instance.set_problem_refs(problem_refs)
        return instance

    def create(self, validated_data):
        instance: models.CrewActivityDAO = super().create(validated_data)
        instance.update_name()
        instance.save()
        return instance


class CrewActivityProblemDAOSerializer(GenericModelToDTOSerializer):
    model_converter_class = converters.CrewActivityProblemDetailConverter
    dto_serializer_class = CrewActivityProblemDetailDTOSerializer

    class Meta:
        model = models.CrewProblemDAO
        fields = []


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
    is_recruiting = serializers.BooleanField()
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


class CrewDAOSerializer(GenericModelToDTOSerializer):
    model_converter_class = converters.CrewDetailConverter
    dto_serializer_class = CrewDetailDTOSerializer

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
            'custom_tags',
            'languages',
        ]

    def save(self, **kwargs):
        instance: models.CrewDAO
        languages = self.validated_data.pop('languages', [])
        with atomic():
            super().save(**kwargs)
            instance = self.instance
            instance.set_submittable_languages(languages)

    def create(self, validated_data):
        validated_data[models.CrewDAO.field_name.CREATED_BY] = self.get_authenticated_user()
        return super().create(validated_data)


class CrewApplicantDTOSerializer(UserDTOSerializer):
    boj = BOJUserDTOSerializer()


class CrewApplicationDTOSerializer(serializers.Serializer):
    application_id = serializers.IntegerField()
    applicant = CrewApplicantDTOSerializer()
    message = serializers.CharField()
    is_pending = serializers.BooleanField()
    is_accepted = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class ReviewedCrewApplicationDTOSerializer(CrewApplicationDTOSerializer):
    reviewed_at = serializers.DateTimeField()
    reviewed_by = UserDTOSerializer()


class CrewApplicationDAOSerializer(GenericModelToDTOSerializer):
    model_converter_class = converters.CrewApplicationConverter
    dto_serializer_class = CrewApplicationDTOSerializer

    class Meta:
        model = models.CrewApplicationDAO
        fields = [
            models.CrewApplicationDAO.field_name.CREW,
            models.CrewApplicationDAO.field_name.MESSAGE,
            models.CrewApplicationDAO.field_name.APPLICANT,
        ]
        extra_kwargs = {
            models.CrewApplicationDAO.field_name.APPLICANT: {'read_only': True},
        }

    def create(self, validated_data):
        validated_data[models.CrewApplicationDAO.field_name.APPLICANT] = self.get_authenticated_user()
        return super().create(validated_data)


class CrewStatisticsDTOSerializer(ProblemStatisticDTOSerializer):
    pass
