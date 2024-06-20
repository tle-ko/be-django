from rest_framework.generics import *
from rest_framework.permissions import *

from user.models import User

from .models import *
from .serializers import *


class CrewAPIView:
    class ListCreate(ListCreateAPIView):
        queryset = Crew.objects.all()
        serializer_class = CrewSerializer
        permission_classes = [IsAuthenticated]

        def perform_create(self, serializer):
            serializer.save(captain=self._get_user())

        def _get_user(self) -> User:
            return User.objects.get(pk=self.request.user.pk)
