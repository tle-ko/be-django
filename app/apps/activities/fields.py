from rest_framework import serializers

from apps.activities.models import CrewActivity


class ActivityProblemsField(serializers.SerializerMethodField):
    def get_attribute(self, instance: CrewActivity):
        return super().get_attribute(instance)