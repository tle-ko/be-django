from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework import validators

from apps.problems.proxy import Problem
from apps.problems.serializers import ProblemDTOSerializer
from apps.submissions.serializers import SubmissionDTOSerializer

from . import proxy


class CrewActivityProblemDTOSerializer(ProblemDTOSerializer):
    problem_ref_id = serializers.IntegerField()
    order = serializers.IntegerField()


class CrewActivityProblemDetailDTOSerializer(CrewActivityProblemDTOSerializer):
    submissions = SubmissionDTOSerializer(many=True)


class CrewActivityProblemExtraDetailDTOSerializer(CrewActivityProblemDetailDTOSerializer):
    my_submission = SubmissionDTOSerializer(required=False, default=None)


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


class CrewActivityDAOSerializer(serializers.ModelSerializer):
    problem_refs = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = proxy.CrewActivity
        fields = [
            proxy.CrewActivity.field_name.START_AT,
            proxy.CrewActivity.field_name.END_AT,
            'problem_refs',
        ]

    @property
    def data(self):
        self.instance: proxy.CrewActivity
        return CrewActivityDetailDTOSerializer(self.instance.as_detail_dto()).data

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
            proxy.CrewActivityProblem.objects.filter(activity=self.instance).delete()
            problems = []
            for order, problem_ref in enumerate(problem_refs, start=1):
                problems.append(proxy.CrewActivityProblem(
                    crew=self.instance.crew,
                    activity=self.instance,
                    problem=problem_ref,
                    order=order,
                ))
            proxy.CrewActivityProblem.objects.bulk_create(problems)
        return self.instance
