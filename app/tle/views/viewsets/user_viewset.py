from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tle.models import User
from tle.serializers import *
from tle.views.permissions import *


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    lookup_field = 'id'

    def current(self, request: Request):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)
