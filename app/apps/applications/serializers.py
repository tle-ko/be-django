from dataclasses import asdict

from rest_framework import serializers

from apps.boj.serializers import BOJUserDTOSerializer
from users.serializers import UserDTOSerializer

from .models import proxy


PK = 'id'


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


class CrewApplicationDAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = proxy.CrewApplication
        fields = [
            proxy.CrewApplication.field_name.CREW,
            proxy.CrewApplication.field_name.MESSAGE,
            proxy.CrewApplication.field_name.APPLICANT,
        ]
        extra_kwargs = {
            proxy.CrewApplication.field_name.APPLICANT: {
                'read_only': True,
                'default': serializers.CurrentUserDefault(),
            },
        }

    @property
    def data(self):
        self.instance: proxy.CrewApplication
        return asdict(self.instance.as_dto())
