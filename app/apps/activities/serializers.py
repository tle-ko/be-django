from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework import validators

from apps.problems.proxy import Problem
from apps.problems.serializers import ProblemDTOSerializer
from apps.problems.serializers import ProblemDetailDTOSerializer
from apps.submissions.serializers import SubmissionDTOSerializer
from common.mixins import SerializerCurrentUserMixin

from . import dto
from . import models


class CrewActivityProblemDTOSerializer(ProblemDTOSerializer):
    __dto__ = dto.CrewActivityProblemDTO

    problem_id = serializers.IntegerField()
    order = serializers.IntegerField()


class CrewActivityProblemDetailDTOSerializer(ProblemDetailDTOSerializer):
    __dto__ = dto.CrewActivityProblemDetailDTO

    problem_id = serializers.IntegerField()
    order = serializers.IntegerField()
    submission_id = serializers.IntegerField()
    has_submitted = serializers.BooleanField()


class CrewActivityProblemExtraDetailDTOSerializer(CrewActivityProblemDTOSerializer):
    submissions = SubmissionDTOSerializer(many=True)
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


class CrewActivityExtraDetailDTOSerializer(CrewActivityDTOSerializer):
    problems = CrewActivityProblemExtraDetailDTOSerializer(many=True)


class CrewActivityDAOSerializer(SerializerCurrentUserMixin, serializers.ModelSerializer):
    problem_refs = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = models.CrewActivityDAO
        fields = [
            models.CrewActivityDAO.field_name.START_AT,
            models.CrewActivityDAO.field_name.END_AT,
            'problem_refs',
        ]

    @property
    def data(self):
        self.instance: models.CrewActivityDAO
        user = self.context['request'].user
        assert user.is_authenticated
        return CrewActivityExtraDetailDTOSerializer(self.instance.as_extra_detail_dto(user)).data

    def save(self, **kwargs):
        problem_ref_ids = self.validated_data.pop('problem_refs')
        problem_refs = []
        try:
            for problem_ref_id in problem_ref_ids:
                problem_ref = Problem.objects.get(pk=problem_ref_id)
                problem_refs.append(problem_ref)
        except Problem.DoesNotExist:
            raise validators.ValidationError(
                f'Invalid problem_ref_id: {problem_ref_id}')
        with atomic():
            super().save(**kwargs)
            models.CrewActivityProblemDAO.objects.filter(activity=self.instance).delete()
            problems = []
            for order, problem_ref in enumerate(problem_refs, start=1):
                problems.append(models.CrewActivityProblemDAO(
                    crew=self.instance.crew,
                    activity=self.instance,
                    problem=problem_ref,
                    order=order,
                ))
            models.CrewActivityProblemDAO.objects.bulk_create(problems)
        return self.instance
