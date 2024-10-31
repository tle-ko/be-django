import typing

from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework import validators

from apps.problems.proxy import Problem
from apps.problems.serializers import ProblemDTOSerializer
from apps.problems.serializers import ProblemDetailDTOSerializer
from apps.submissions.serializers import SubmissionDTOSerializer
from common.serializers import GenericModelToDTOSerializer

from . import converters
from . import models


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

    def get_model_converter(self, *args, **kwargs):
        return converters.CrewActivityDetailConverter(self.get_authenticated_user())

    def save(self, **kwargs):
        # Save problems
        problem_ref_ids: typing.List[int]
        problem_ref_ids = self.validated_data.pop('problem_refs')
        problem_ref_id_to_order = {
            problem_ref_id: order for order, problem_ref_id in enumerate(problem_ref_ids, start=1)
        }
        try:
            with atomic():
                instance: models.CrewActivityDAO = super().save(**kwargs)
                old = self._old_problems(instance)
                new = self._new_problems(
                    instance, problem_ref_ids, order_start_at=len(old))
                for deleted_obj in (old - new):
                    deleted_obj.delete()
                for obj in new:
                    obj.order = problem_ref_id_to_order[obj.problem.pk]
                    obj.save()
        except models.models.deletion.ProtectedError:
            raise validators.ValidationError({
                'message': f'Cannot delete problems that are already submitted.',
                'object': f'<CrewActivityProblem id={deleted_obj.pk} ref_id={deleted_obj.problem.pk} title={deleted_obj.problem.title}>',
                'jobs': {
                    'refs to add': [obj.problem.pk for obj in (new - old)],
                    'refs to remove': [obj.problem.pk for obj in (old - new)],
                    'refs to keep': [obj.problem.pk for obj in (old & new)],
                }
            })
        return instance

    def create(self, validated_data):
        return super().create({
            **validated_data,
            models.CrewActivityDAO.field_name.NAME: self._default_name(validated_data[models.CrewActivityDAO.field_name.CREW]),
        })

    def _default_name(self, crew: models.CrewDAO) -> str:
        count = models.CrewActivityDAO.objects \
            .filter(**{models.CrewActivityDAO.field_name.CREW: crew}) \
            .count()
        return f'{count+1}회차'

    def _old_problems(self, instance: models.CrewActivityDAO) -> typing.Set[models.CrewActivityProblemDAO]:
        return set(models.CrewActivityProblemDAO.objects.filter(**{
            models.CrewActivityProblemDAO.field_name.ACTIVITY: instance,
        }))

    def _new_problems(self, instance: models.CrewActivityDAO, problem_ref_ids: typing.List[int], order_start_at: int) -> typing.Set[models.CrewActivityProblemDAO]:
        objects = set()
        for order, problem_ref_id in enumerate(problem_ref_ids, start=order_start_at):
            obj = None
            try:
                problem = Problem.objects \
                    .filter(**{Problem.field_name.CREATED_BY: self.get_authenticated_user()}) \
                    .get(**{Problem.field_name.PK: problem_ref_id})
            except Problem.DoesNotExist:
                raise validators.ValidationError(
                    f'Invalid problem_ref_id: {problem_ref_id}',
                )
            try:
                obj = models.CrewActivityProblemDAO.objects.get(**{
                    models.CrewActivityProblemDAO.field_name.ACTIVITY: instance,
                    models.CrewActivityProblemDAO.field_name.PROBLEM: problem,
                })
            except models.CrewActivityProblemDAO.DoesNotExist:
                obj = models.CrewActivityProblemDAO.objects.create(**{
                    models.CrewActivityProblemDAO.field_name.CREW: instance.crew,
                    models.CrewActivityProblemDAO.field_name.ACTIVITY: instance,
                    models.CrewActivityProblemDAO.field_name.PROBLEM: problem,
                    models.CrewActivityProblemDAO.field_name.ORDER: order,
                })
            assert obj is not None
            objects.add(obj)
        return objects


class CrewActivityProblemDAOSerializer(GenericModelToDTOSerializer):
    model_converter_class = converters.CrewActivityProblemDetailConverter
    dto_serializer_class = CrewActivityProblemDetailDTOSerializer

    class Meta:
        model = models.CrewActivityProblemDAO
        fields = []

    def get_model_converter(self, *args, **kwargs) -> converters.ModelConverter:
        return super().get_model_converter(self.get_authenticated_user())
