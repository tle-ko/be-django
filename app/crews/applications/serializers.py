from rest_framework import serializers

from crews.applications.models import CrewApplication


PK = 'id'


class NoInputSerializer(serializers.Serializer):
    pass


class CrewApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewApplication
        read_only_fields = ['__all__']


class CrewApplicationCreateSerializer(serializers.ModelSerializer):
    message = serializers.CharField()

    class Meta:
        model = CrewApplication
        fields = [
            CrewApplication.field_name.MESSAGE,
        ]
        read_only_fields = ['__all__']


## TEMP

# class CrewApplicationAboutApplicantSerializer(serializers.ModelSerializer):
#     applicant = fields.CrewApplicationApplicantField()

#     class Meta:
#         model = models.CrewApplication
#         fields = [
#             PK,
#             models.CrewApplication.field_name.MESSAGE,
#             models.CrewApplication.field_name.IS_PENDING,
#             models.CrewApplication.field_name.IS_ACCEPTED,
#             models.CrewApplication.field_name.CREATED_AT,
#             'applicant',
#         ]
#         read_only_fields = ['__all__']


# class CrewApplicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.CrewApplication


# class CrewApplicationCreateSerializer(serializers.ModelSerializer):
#     message = serializers.CharField()

#     class Meta:
#         model = models.CrewApplication
#         fields = [
#             models.CrewApplication.field_name.MESSAGE,
#         ]
#         read_only_fields = ['__all__']