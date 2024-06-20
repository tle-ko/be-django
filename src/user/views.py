from rest_framework.generics import *
from rest_framework.permissions import *

from .models import *
from .serializers import *


class UserAPIView:
    class ListCreate(ListCreateAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [IsAdminUser]
