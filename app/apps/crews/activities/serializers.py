from rest_framework import serializers

from apps.crews.activities.models import CrewActivity


PK = 'id'


class CrewActivitySerializer(serializers.ModelSerializer):
    date_start_at = serializers.DateField(source=CrewActivity.field_name.START_AT)
    date_end_at = serializers.DateField(source=CrewActivity.field_name.END_AT)

    class Meta:
        model = CrewActivity
        fields = [
            CrewActivity.field_name.NAME,
            'date_start_at',
            'date_end_at',
        ]
        read_only_fields = ['__all__']


# class CrewActivityProblemSerializer(serializers.ModelSerializer):
#     problems = fields.CrewAcitivityProblemsField()

#     class Meta:
#         model = CrewActivity
#         fields = [
#             CrewActivity.field_name.NAME,
#             CrewActivity.field_name.START_AT,
#             CrewActivity.field_name.END_AT,
#             'problems',
#         ]
#         read_only_fields = ['__all__']
