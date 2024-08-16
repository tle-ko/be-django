from rest_framework import generics
from rest_framework import permissions

from problems import models
from problems import serializers


class ProblemCreateAPIView(generics.CreateAPIView):
    """문제 생성 API"""

    queryset = models.Problem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProblemDetailSerializer


class ProblemDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """문제 상세 조회, 수정, 삭제 API"""

    queryset = models.Problem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProblemDetailSerializer
    lookup_field = 'id'


class ProblemSearchListAPIView(generics.ListAPIView):
    """문제 검색 API"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProblemMinimalSerializer

    def get_queryset(self):
        return models.Problem.objects.filter(**{
            models.Problem.field_name.CREATED_BY: self.request.user,
        })
