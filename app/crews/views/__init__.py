from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from crews.models import Crew, CrewMember
from crews import serializers
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


class CrewDashboard(generics.RetrieveAPIView):
    """가입한 크루 목록 조회 API"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewDashboardSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return Response(
            data={
                'id': 1,
                'icon': '😀',
                'name': '코딩메리호',
                'activity': {
                    'recent': {
                        'id': 1,
                        'name': '9회차',
                        'problems': {
                            'count': 8,
                            'items': [
                                {
                                    'problem_number': 1,
                                    'is_solved': False,
                                },
                                {
                                    'problem_number': 2,
                                    'is_solved': False,
                                },
                                {
                                    'problem_number': 3,
                                    'is_solved': True,
                                },
                                {
                                    'problem_number': 4,
                                    'is_solved': True,
                                },
                                {
                                    'problem_number': 5,
                                    'is_solved': True,
                                },
                                {
                                    'problem_number': 6,
                                    'is_solved': True,
                                },
                                {
                                    'problem_number': 7,
                                    'is_solved': True,
                                },
                                {
                                    'problem_number': 8,
                                    'is_solved': True,
                                },
                            ],
                        },
                    },
                },
                'members': {
                    'count': 3,
                    'max_count': 8,
                    'items': [
                        {
                            "id": 4,
                            "username": "hey",
                            "profile_image": "https://picsum.photos/250/250",
                            "is_captain": True,
                        },
                        {
                            "id": 3,
                            "username": "hello",
                            "profile_image": "https://picsum.photos/250/250",
                            "is_captain": False,
                        },
                        {
                            "id": 2,
                            "username": "hi",
                            "profile_image": "https://picsum.photos/250/250",
                            "is_captain": False,
                        },
                    ],
                },
                'member_submissions': {
                    'count': 2,
                    'items': [
                        {
                            'user_id': 1,
                            "username": "hey",
                            "submissions": {
                                'count': 7,
                                'items': [
                                    {
                                        'problem_number': 1,
                                        'submission_id': 1,
                                        'is_correct': True,
                                        'is_help_needed': False,
                                    },
                                    {
                                        'problem_number': 2,
                                        'submission_id': 2,
                                        'is_correct': False,
                                        'is_help_needed': True,
                                    },
                                    {
                                        'problem_number': 4,
                                        'submission_id': 3,
                                        'is_correct': True,
                                        'is_help_needed': False,
                                    },
                                    {
                                        'problem_number': 5,
                                        'submission_id': 4,
                                        'is_correct': True,
                                        'is_help_needed': False,
                                    },
                                    {
                                        'problem_number': 6,
                                        'submission_id': 5,
                                        'is_correct': True,
                                        'is_help_needed': False,
                                    },
                                    {
                                        'problem_number': 7,
                                        'submission_id': 6,
                                        'is_correct': True,
                                        'is_help_needed': False,
                                    },
                                    {
                                        'problem_number': 8,
                                        'submission_id': 7,
                                        'is_correct': True,
                                        'is_help_needed': False,
                                    },
                                ],
                            },
                        },
                        {
                            'user_id': 2,
                            "username": "leeyuuuuuuum",
                            "submissions": {
                                'count': 6,
                                'items': [
                                    {
                                        'problem_number': 1,
                                        'submission_id': 8,
                                        'is_correct': False,
                                        'is_help_needed': True,
                                    },
                                    {
                                        'problem_number': 2,
                                        'submission_id': 9,
                                        'is_correct': True,
                                        'is_help_needed': True,
                                    },
                                    {
                                        'problem_number': 4,
                                        'submission_id': 10,
                                        'is_correct': True,
                                        'is_help_needed': False,
                                    },
                                    {
                                        'problem_number': 5,
                                        'submission_id': 11,
                                        'is_correct': False,
                                        'is_help_needed': False,
                                    },
                                    {
                                        'problem_number': 7,
                                        'submission_id': 12,
                                        'is_correct': True,
                                        'is_help_needed': False,
                                    },
                                    {
                                        'problem_number': 8,
                                        'submission_id': 13,
                                        'is_correct': True,
                                        'is_help_needed': False,
                                    },
                                ],
                            },
                        }
                    ],
                },
                'tags': {
                    'count': 3,
                    'items': [
                        {
                            'key': 'python',
                            'name': 'Python',
                            'type': 'language',
                        },
                        {
                            'key': None,
                            'name': '실버 이상',
                            'type': 'level',
                        },
                        {
                            'key': None,
                            'name': '우하하',
                            'type': 'custom',
                        },
                    ],
                },
                'statistics': {
                    'difficulty': [
                        {
                            'difficulty': 1,
                            'problem_count': 3,
                            'ratio': .375,
                        },
                        {
                            'difficulty': 2,
                            'problem_count': 3,
                            'ratio': .375,
                        },
                        {
                            'difficulty': 3,
                            'problem_count': 2,
                            'ratio': .25,
                        }
                    ],
                    'tags': [
                        {
                            'label': {
                                'en': 'mathematics',
                                'ko': '수학'
                            },
                            'problem_count': 20,
                            'ratio': .392,
                        },
                        {
                            'label': {
                                'en': 'implementation',
                                'ko': '구현'
                            },
                            'problem_count': 20,
                            'ratio': .392,
                        },
                        {
                            'label': {
                                'en': 'graph',
                                'ko': '그래프 이론'
                            },
                            'problem_count': 5,
                            'ratio': .098,
                        },
                        {
                            'label': {
                                'en': 'dynamic programming',
                                'ko': '다이나믹 프로그래밍'
                            },
                            'problem_count': 4,
                            'ratio': .078,
                        },
                        {
                            'label': {
                                'en': 'data structures',
                                'ko': '자료구조'
                            },
                            'problem_count': 4,
                            'ratio': .078,
                        },
                    ],
                },
                'reviews': {
                    'count': 2,
                    'items': [
                        {
                            'problem_number': 1,
                            'problem_title': 'A+B',
                            'submission_id': 1,
                            'submission_created_at': timezone.now(),
                            'reviewers': {
                                'count': 3,
                                'items': [
                                    {
                                        "id": 4,
                                        "username": "hey",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                    {
                                        "id": 3,
                                        "username": "hello",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                    {
                                        "id": 2,
                                        "username": "hi",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                ],
                            },
                        },
                        {
                            'problem_number': 2,
                            'problem_title': 'C+D',
                            'submission_id': 2,
                            'submission_created_at': timezone.now(),
                            'reviewers': {
                                'count': 1,
                                'items': [
                                    {
                                        "id": 4,
                                        "username": "hey",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                ],
                            },
                        },
                        {
                            'problem_number': 3,
                            'problem_title': '임시제목',
                            'submission_id': 3,
                            'submission_created_at': timezone.now(),
                            'reviewers': {
                                'count': 1,
                                'items': [
                                    {
                                        "id": 4,
                                        "username": "hey",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                ],
                            },
                        },
                        {
                            'problem_number': 4,
                            'problem_title': '임시제목',
                            'submission_id': 4,
                            'submission_created_at': timezone.now(),
                            'reviewers': {
                                'count': 1,
                                'items': [
                                    {
                                        "id": 4,
                                        "username": "hey",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                ],
                            },
                        },
                        {
                            'problem_number': 5,
                            'problem_title': '임시제목',
                            'submission_id': 5,
                            'submission_created_at': timezone.now(),
                            'reviewers': {
                                'count': 1,
                                'items': [
                                    {
                                        "id": 4,
                                        "username": "hey",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                ],
                            },
                        },
                        {
                            'problem_number': 6,
                            'problem_title': '임시제목',
                            'submission_id': 6,
                            'submission_created_at': timezone.now(),
                            'reviewers': {
                                'count': 1,
                                'items': [
                                    {
                                        "id": 4,
                                        "username": "hey",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                ],
                            },
                        },
                        {
                            'problem_number': 7,
                            'problem_title': '임시제목',
                            'submission_id': 7,
                            'submission_created_at': timezone.now(),
                            'reviewers': {
                                'count': 1,
                                'items': [
                                    {
                                        "id": 4,
                                        "username": "hey",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                ],
                            },
                        },
                        {
                            'problem_number': 8,
                            'problem_title': '임시제목',
                            'submission_id': 8,
                            'submission_created_at': timezone.now(),
                            'reviewers': {
                                'count': 1,
                                'items': [
                                    {
                                        "id": 4,
                                        "username": "hey",
                                        "profile_image": "https://picsum.photos/250/250",
                                    },
                                ],
                            },
                        },
                    ],
                },
            },
        )