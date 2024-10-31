from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status

from . import models
from . import permissions
from . import serializers


class CrewActivityCreateAPIView(generics.CreateAPIView):
    """크루 활동 생성 API.\n\n."""
    queryset = models.CrewDAO
    serializer_class = serializers.CrewActivityDAOSerializer
    permission_classes = [permissions.IsCaptain]
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: serializer_class.dto_serializer_class})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: serializers.CrewActivityDAOSerializer):
        serializer.save(**{
            models.CrewActivityDAO.field_name.CREW: self.get_object(),
        })


class CrewActivityRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """크루 활동 상세 조회 API.\n\n."""
    queryset = models.CrewActivityDAO
    serializer_class = serializers.CrewActivityDAOSerializer
    permission_classes = [permissions.IsCaptain |
                          permissions.IsMemberAndReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: serializer_class.dto_serializer_class})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class CrewActivityProblemRetrieveAPIView(generics.RetrieveAPIView):
    """크루 활동 문제 상세 조회 API.\n\n."""
    queryset = models.CrewActivityProblemDAO
    serializer_class = serializers.CrewActivityProblemDAOSerializer
    permission_classes = [permissions.IsMemberAndReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'problem_id'

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
