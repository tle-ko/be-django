from django.test import TestCase
from rest_framework import status

from users.models import User

from . import models


class ProblemCreateAPIViewTest(TestCase):
    fixtures = [
        'fixtures/tests/users.json',
    ]
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.fields = {
            "title": "Test Problem",
            "link": "https://boj.kr/1000",
            "description": "테스트용 문제입니다.",
            "input_description": "입력이 없습니다.",
            "output_description": "출력이 없습니다.",
            "memory_limit": 0,
            "time_limit": 0,
        }
        self.required_fields = [
            "title",
            "description",
            "input_description",
            "output_description",
            "memory_limit",
            "time_limit",
        ]

    def test_201_문제_생성(self):
        res = self.client.post("/api/v1/problem_ref", self.fields)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_401_비로그인_사용_불가(self):
        self.client.logout()
        res = self.client.post("/api/v1/problem_ref", self.fields)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_201_링크가_누락_되어도_문제_생성_가능(self):
        del self.fields['link']
        res = self.client.post("/api/v1/problem_ref", self.fields)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_400_제목_누락(self):
        del self.fields['title']
        res = self.client.post("/api/v1/problem_ref", self.fields)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ProblemDetailRetrieveAPIViewTest(TestCase):
    fixtures = [
        'fixtures/tests/users.json',
        'fixtures/tests/problems.json',
    ]
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_200_내가_만든_문제(self):
        problem = models.ProblemDAO.objects.get(pk=1)
        self.assertEqual(problem.created_by, self.user)

        res = self.client.get(f"/api/v1/problem_ref/{problem.pk}/detail")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_403_내가_만들지_않은_문제(self):
        problem = models.ProblemDAO.objects.get(pk=2)
        self.assertNotEqual(problem.created_by, self.user)

        res = self.client.get(f"/api/v1/problem_ref/{problem.pk}/detail")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class ProblemSearchListAPIViewTest(TestCase):
    fixtures = [
        'fixtures/tests/users.json',
        'fixtures/tests/problems.json',
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_200_모든_문제_가져오기(self):
        res = self.client.get("/api/v1/problem_refs")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('results', res.json())

        my_problems = models.ProblemDAO.objects.filter(**{
            models.ProblemDAO.field_name.CREATED_BY: self.user,
        })
        self.assertEqual(len(res.json()['results']), my_problems.count())
