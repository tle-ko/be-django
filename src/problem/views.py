from rest_framework.generics import *
from rest_framework.permissions import *

from .models import *
from .serializers import *


class ProblemAPIView:
    class ListCreate(ListCreateAPIView):
        queryset = Problem.objects.all()
        serializer_class = ProblemSerializer
        permission_classes = [IsAuthenticated]
