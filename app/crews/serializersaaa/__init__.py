from django.db.transaction import atomic
from rest_framework import serializers

from crews import enums
from crews import models
from crews import servicesa
from crews.serializersaaa import fields


PK = 'id'


class NoInputSerializer(serializers.Serializer):
    pass



# Crew Retrieve Serializers

class CrewRecruitingSerializer(serializers.ModelSerializer):
    ...


class CrewJoinedSerializer(serializers.ModelSerializer):
    ...


class CrewDashboardSerializer(serializers.ModelSerializer):
    ...


class CrewCreateSerializer(serializers.ModelSerializer):
    ...