from typing import Callable

from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.serializers import Serializer
from rest_framework.response import Response

from submissions import serializers


class CreateCodeReview(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.SubmissionSerializer
    get_serializer: Callable[..., Serializer]

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