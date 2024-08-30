from django.test import TestCase
from rest_framework import status

from users.models import User


class CrewAPITest(TestCase):
    fixtures = ['sample.json']
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_비로그인_사용자로_recruiting_크루_목록_조회(self):
        self.client.logout()
        res = self.client.get("/api/v1/crews/recruiting")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(res.json(), [
            {
                "id": 1,
                "icon": "🚢",
                "name": "코딩메리호",
                "is_joinable": False,
                "is_active": True,
                "members": {"count": 1, "max_count": 8},
                "tags": [
                    {"type": "language", "key": "java",     "name": "Java"},
                    {"type": "language", "key": "kotlin",   "name": "Kotlin"},
                    {"type": "level",    "key": None,       "name": "실버 이상"},
                    {"type": "custom",   "key": None,       "name": "삼성코테준비"},
                    {"type": "custom",   "key": None,       "name": "상명인 모여라"}
                ],
                "latest_activity": {
                    "name": "등록된 활동 없음",
                    "date_start_at": None,
                    "date_end_at": None
                }
            },
            {
                "id": 2,
                "icon": "🚢",
                "name": "다른사람이크루장",
                "is_joinable": False,
                "is_active": True,
                "members": {"count": 1, "max_count": 6},
                "tags": [
                    {"type": "language", "key": "python",   "name": "Python"},
                    {"type": "level",    "key": None,       "name": "브론즈 4 이상"},
                ],
                "latest_activity": {
                    "name": "등록된 활동 없음",
                    "date_start_at": None,
                    "date_end_at": None
                }
            },
        ])

    def test_로그인_사용자로_recruiting_크루_목록_조회(self):
        res = self.client.get("/api/v1/crews/recruiting")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(res.json(), [
            {
                "id": 2,
                "icon": "🚢",
                "name": "다른사람이크루장",
                "is_joinable": True,
                "is_active": True,
                "members": {"count": 1, "max_count": 6},
                "tags": [
                    {"type": "language", "key": "python",   "name": "Python"},
                    {"type": "level",    "key": None,       "name": "브론즈 4 이상"},
                ],
                "latest_activity": {
                    "name": "등록된 활동 없음",
                    "date_start_at": None,
                    "date_end_at": None
                }
            },
        ])

    def test_비로그인_사용자로_my_크루_목록_조회_불가능(self):
        self.client.logout()
        res = self.client.get("/api/v1/crews/my")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_my_크루_목록_조회(self):
        res = self.client.get("/api/v1/crews/my")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(res.json(), [
            {
                "id": 1,
                "icon": "🚢",
                "name": "코딩메리호",
                "is_active": True,
                "latest_activity": {
                    "name": "등록된 활동 없음",
                    "date_start_at": None,
                    "date_end_at": None
                }
            },
        ])
