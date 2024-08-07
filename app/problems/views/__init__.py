from rest_framework import mixins
from rest_framework import permissions
from rest_framework.generics import GenericAPIView

from problems.models import Problem
from problems.serializers import ProblemDetailSerializer, ProblemMinimalSerializer


class ProblemCreate(mixins.CreateModelMixin,
                    GenericAPIView):
    """문제 생성 API"""

    queryset = Problem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProblemDetailSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProblemDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericAPIView):
    """문제 상세 조회, 수정, 삭제 API"""

    queryset = Problem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProblemDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProblemSearch(mixins.ListModelMixin,
                    GenericAPIView):
    """문제 검색 API"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProblemMinimalSerializer

    def get_queryset(self):
        return Problem.objects.filter(**{
            Problem.field_name.CREATED_BY: self.request.user,
        })

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
