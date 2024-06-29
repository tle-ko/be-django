import logging

from rest_framework.generics import *
from rest_framework.permissions import *

from user.models import User

from .models import *
from .serializers import *


logger = logging.getLogger(__name__)


def _get_user(view: GenericAPIView) -> User:
    user = view.request.user
    try:
        return User.objects.get(pk=user.pk)
    except User.DoesNotExist:
        logger.error(f'User not found. {user.pk}')
        logger.error(
            f'checking user model... '
            f'expected: {User.__class__} '
            f'actual: {user.__class__}'
        )
        return None


class CrewAPIView:
    class ListCreate(ListCreateAPIView):
        queryset = Crew.objects.all()
        serializer_class = CrewSerializer
        permission_classes = [IsAuthenticated]

        def perform_create(self, serializer):
            serializer.save(captain=_get_user(self))

    class MyList(ListAPIView):
        """내가 속한 크루의 목록을 반환합니다."""
        serializer_class = CrewSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            return _get_user(self).crews.all()

    class RecruitingList(ListAPIView):
        """현재 참가자를 모집 중인 크루의 목록을 반환합니다."""
        serializer_class = CrewSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            # TODO: 언어, 티어 조건에 따라 필터링
            return Crew.objects.filter(is_recruiting=True)

    class RetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
        queryset = Crew.objects.all()
        serializer_class = CrewSerializer
        permission_classes = [IsAuthenticated]
        lookup_url_kwarg = 'id'
