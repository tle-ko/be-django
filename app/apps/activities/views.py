from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status

from . import mixins
from . import permissions
from . import proxy
from . import serializers


class CrewActivityCreateAPIView(mixins.CrewUrlKwargMixin, generics.CreateAPIView):
    """크루 활동 생성 API.\n\n."""
    serializer_class = serializers.CrewActivityDAOSerializer
    permission_classes = [permissions.IsCaptain]

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: serializers.CrewActivityDetailDTOSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: serializers.CrewActivityDAOSerializer):
        crew = self.get_object()
        name = f'{proxy.CrewActivity.objects.filter(crew=crew).count()+1} 회차'
        serializer.save(**{
            proxy.CrewActivity.field_name.CREW: crew,
            proxy.CrewActivity.field_name.NAME: name,
        })


class CrewActivityRetrieveUpdateAPIView(mixins.CrewActivityUrlKwargMixin, generics.RetrieveUpdateAPIView):
    """크루 활동 상세 조회 API.\n\n."""
    serializer_class = serializers.CrewActivityDAOSerializer
    permission_classes = [permissions.IsCaptain | permissions.IsMemberAndReadOnly]

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: serializers.CrewActivityProblemDetailDTOSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewActivityExtraDetailDTOSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewActivityExtraDetailDTOSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class CrewActivityProblemRetrieveAPIView(mixins.CrewActivityProblemUrlKwargMixin, generics.RetrieveAPIView):
    """크루 활동 문제 상세 조회 API.\n\n."""
    serializer_class = serializers.CrewActivityProblemDetailDTOSerializer
    permission_classes = [permissions.IsMemberAndReadOnly]

    def get_object(self):
        return super().get_object().as_detail_dto()
