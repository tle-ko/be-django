from rest_framework.generics import *
from rest_framework.permissions import *

from config.permissions import *

from .models import *
from .serializers import *


class TagAPIView:
    class ListCreate(ListCreateAPIView):
        queryset = Tag.objects.all()
        serializer_class = TagSerializer
        permission_classes = [IsAdminUser|ReadOnly]
