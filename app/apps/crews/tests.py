import datetime

from django.test import TestCase
from rest_framework import status

from apps.problems.enums import ProblemDifficulty

from . import models


class RecruitingCrewListAPIViewTest(TestCase):
    fixtures = ['tests/users.json', 'tests/crews.json']
    maxDiff = None

    def setUp(self) -> None:
        self.user = models.User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_200_비로그인_사용자로_recruiting_크루_목록_조회(self):
        self.client.logout()
        res = self.client.get("/api/v1/crews/recruiting")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[1]["id"], 2)

    def test_200_로그인_사용자로_recruiting_크루_목록_조회(self):
        res = self.client.get("/api/v1/crews/recruiting")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(res.json(), [
            {
                "id": 2,
                "crew_id": 2,
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
                    "start_at": None,
                    "end_at": None
                }
            },
        ])


class MyCrewListAPIViewTest(TestCase):
    fixtures = ['sample.json']
    maxDiff = None

    def setUp(self) -> None:
        self.user = models.User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_401_비로그인_사용자로_my_크루_목록_조회_불가능(self):
        self.client.logout()
        res = self.client.get("/api/v1/crews/my")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_200_my_크루_목록_조회(self):
        res = self.client.get("/api/v1/crews/my")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(res.json(), [
            {
                "id": 1,
                "crew_id": 1,
                "icon": "🚢",
                "name": "코딩메리호",
                "is_active": True,
                "latest_activity": {
                    "name": "등록된 활동 없음",
                    "start_at": None,
                    "end_at": None
                }
            },
        ])


class CrewCreateAPIViewTest(TestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = models.User.objects.create(**{
            models.User.field_name.USERNAME: "test",
            models.User.field_name.PASSWORD: "test",
            models.User.field_name.EMAIL: "test@example.com",
            models.User.field_name.BOJ_USERNAME: "test",
        })
        cls.crew = models.CrewDAO.objects.create(**{
            models.CrewDAO.field_name.ICON: "🚢",
            models.CrewDAO.field_name.NAME: "코딩메리호",
            models.CrewDAO.field_name.IS_ACTIVE: True,
            models.CrewDAO.field_name.CREATED_BY: cls.user,
        })

    def setUp(self) -> None:
        self.user = models.User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_201_크루_생성(self):
        res = self.client.post("/api/v1/crew", {
            "icon": "🥇",
            "name": "임시로 생성해본 크루",
            "max_members": 3,
            "languages": [
                "java",
            ],
            "min_boj_level": 0,
            "custom_tags": ['tag1'],
            "notice": "string",
            "is_recruiting": True,
            "is_active": True
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.json())


class CrewStatisticsAPIViewTest(TestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = models.User.objects.create(**{
            models.User.field_name.USERNAME: "test",
            models.User.field_name.PASSWORD: "test",
            models.User.field_name.EMAIL: "test@example.com",
        })
        cls.problem_ref = models.ProblemDAO.objects.create(**{
            models.ProblemDAO.field_name.TITLE: "문제1",
            models.ProblemDAO.field_name.DESCRIPTION: "문제1",
            models.ProblemDAO.field_name.INPUT_DESCRIPTION: "문제1",
            models.ProblemDAO.field_name.OUTPUT_DESCRIPTION: "문제1",
            models.ProblemDAO.field_name.TIME_LIMIT: 1,
            models.ProblemDAO.field_name.MEMORY_LIMIT: 128,
            models.ProblemDAO.field_name.CREATED_BY: cls.user,
        })
        cls.analysis = cls.problem_ref.add_analysis(ProblemDifficulty.NORMAL)
        cls.crew = models.CrewDAO.objects.create(**{
            models.CrewDAO.field_name.ICON: "🚢",
            models.CrewDAO.field_name.NAME: "코딩메리호",
            models.CrewDAO.field_name.IS_ACTIVE: True,
            models.CrewDAO.field_name.CREATED_BY: cls.user,
        })
        cls.activity = cls.crew.add_activity("활동1", datetime.datetime(2021, 1, 1, 0, 0, 0), datetime.datetime(2021, 1, 1, 1, 0, 0))
        cls.activity.set_problem_refs([cls.problem_ref])


    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_200_ok(self) -> None:
        res = self.client.get(f"/api/v1/crew/{self.crew.pk}/statistics")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_200_응답_데이터_형식_검사(self) -> None:
        res = self.client.get("/api/v1/crew/{self.crew.pk}/statistics")
        data = res.json()
        self.assertEqual(data["problem_count"], 1)
