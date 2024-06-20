from rest_framework.serializers import *

from .models import *


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
