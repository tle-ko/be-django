from typing import Callable
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.crews.submissions import serializers
from apps.crews.activities.models import CrewActivitySubmission
from apps.crews.submissions.models import SubmissionComment
from users.models import User


class CreateCodeReview(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.SubmissionSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'OK',
            status.HTTP_404_NOT_FOUND: 'Not Found',
        },
    )
    def get(self, request, *args, **kwargs):
        return Response(
            data={
                'id': 1,
                'code': """# 이동3-2\n\n\nimport math\n\n\nMAX_K = math.ceil(math.log(1e9, 3))\n\n\nK_POW = [1]\nfor i in range(1, MAX_K):\n    K_POW.append(3*K_POW[i-1])\n\n\ndef solve(x: int, y: int, k=0) -> bool:\n\n    if k >= MAX_K:\n        return False\n    if x == 0 and y == 0:\n        return True\n    coords = [\n        (x-K_POW[k], y),\n        (x, y-K_POW[k]),\n        (x+K_POW[k], y),\n        (x, y+K_POW[k]),\n    ]\n    for x, y in coords:\n        if k+1 < MAX_K and not (0 < abs(x) < K_POW[k+1] and 0 < abs(y) < K_POW[k+1]):\n            if solve(x, y, k+1):\n                return True\n    return False\n\n\nif __name__ == "__main__":\n    X, Y = map(int, input().split())\n    print('1' if solve(X, Y) else '0')\n""",
                'language': 'python',
                'is_correct': False,
                'is_help_needed': True,
                "created_by": {
                    "id": 2,
                    "username": "hi",
                    "profile_image": "https://picsum.photos/250/250",
                },
                'created_at': timezone.now(),
                'comments': {
                    'count': 1,
                    'items': [
                        {
                            "id": 1,
                            "line_start": 1,
                            "line_end": 3,
                            "content": "이 라인이 조금 이상해요.",
                            "created_by": {
                                "id": 2,
                                "username": "hi",
                                "profile_image": "https://picsum.photos/250/250",
                            },
                        },
                        {
                            "id": 2,
                            "line_start": 2,
                            "line_end": 3,
                            "content": "ㄹㅇ.",
                            "created_by": {
                                "id": 3,
                                "username": "hey",
                                "profile_image": "https://picsum.photos/250/250",
                            },
                        },
                    ]
                },
            },
            status=status.HTTP_200_OK,
        )

# 코드 리뷰 조회 api
class CodeReviewInquiryAPI(APIView):
    def get(self, request, crew_id, user_id):
        user = get_object_or_404(User, id=user_id)

        # CrewActivitySubmission을 필터링
        submissions = CrewActivitySubmission.objects.filter(user=user, problem__crew_id=crew_id).select_related('problem')

        if not submissions.exists():
            return Response({'detail': 'No submissions found.'}, status=status.HTTP_404_NOT_FOUND)

        problems = {}
        for submission in submissions:
            problem_id = submission.problem.id

            if problem_id not in problems:
                # 해당 제출물에 달린 댓글 조회
                comments = SubmissionComment.objects.filter(submission__id=submission.id)

                # 댓글 작성자 정보를 리뷰어로 설정
                reviewers = [
                    {
                        'user_id': comment.created_by.id,
                        'username': comment.created_by.username,
                        'profile_image': comment.created_by.profile_image.url if comment.created_by.profile_image else None
                    }
                    for comment in comments
                ] if comments.exists() else None

                # 문제 정보와 리뷰어 정보를 함께 저장
                problems[problem_id] = {
                    'submission_id': submission.id,
                    'problems_order': submission.problem.order,
                    'problems_title': submission.problem.problem.title,
                    'submission_date': submission.created_at.isoformat(),
                    'reviewers': reviewers  # 댓글 없을 시 None
                }

        # 최종 응답 데이터
        response_data = {
            'members': [
                {
                    'user_id': user.id,
                    'username': user.username,
                    'profile_image': user.profile_image.url if user.profile_image else None,
                    'problems': list(problems.values())
                }
            ]
        }

        return Response(response_data, status=status.HTTP_200_OK)

