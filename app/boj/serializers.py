from rest_framework import serializers

from boj.enums import BOJLevel
from boj.models import BOJUser


class BOJLevelField(serializers.SerializerMethodField):
    def to_representation(self, instance: BOJUser):
        assert isinstance(instance, BOJUser)
        level = BOJLevel(instance.level)
        return {
            'value': level.value,
            'name': level.get_name(lang='ko', arabic=False),
        }


class BOJProfileUrlField(serializers.SerializerMethodField):
    def to_representation(self, instance: BOJUser):
        assert isinstance(instance, BOJUser)
        return f'https://boj.kr/{instance.username}'


class BOJUserSerializer(serializers.ModelSerializer):
    level = BOJLevelField()
    profile_url = BOJProfileUrlField()

    class Meta:
        model = BOJUser
        fields = [
            BOJUser.field_name.USERNAME,
            'profile_url',
            'level',
            BOJUser.field_name.RATING,
            BOJUser.field_name.UPDATED_AT,
        ]
