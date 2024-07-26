from rest_framework import mixins
from rest_framework import permissions
from rest_framework.generics import GenericAPIView

from crews.models import Crew, CrewMember
from crews.serializers import (
    CrewDetailSerializer,
    CrewRecruitingSerializer,
    CrewJoinedSerializer,
)


class CrewCreate(mixins.CreateModelMixin,
                 GenericAPIView):
    """크루 생성 API"""

    queryset = Crew.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewDetailSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class CrewDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericAPIView):
    """크루 상세 조회, 수정, 삭제 API"""

    queryset = Crew.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CrewRecruiting(mixins.ListModelMixin,
                     GenericAPIView):
    """모집 중인 크루 목록 조회 API"""

    queryset = Crew.objects.filter(**{Crew.field_name.IS_RECRUITING: True})
    permission_classes = [permissions.AllowAny]
    serializer_class = CrewRecruitingSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CrewJoined(mixins.ListModelMixin,
                 GenericAPIView):
    """가입한 크루 목록 조회 API"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewJoinedSerializer

    def get_queryset(self):
        # 현재 사용자가 속한 크루만 반환
        crews = CrewMember.objects.filter(**{
            CrewMember.field_name.USER: self.request.user,
        }).values_list(CrewMember.field_name.CREW)
        queryset = Crew.objects.filter(pk__in=crews)
        # 활동 종료된 크루는 뒤로 가도록 정렬
        return queryset.order_by('-'+Crew.field_name.IS_ACTIVE)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
