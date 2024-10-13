from django.test import TestCase
from rest_framework import status

from users.models import User

from . import models


class ProblemCreateAPIViewTest(TestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(**{
            User.field_name.USERNAME: "test",
            User.field_name.PASSWORD: "test",
            User.field_name.EMAIL: "test@example.com",
            User.field_name.BOJ_USERNAME: "test",
        })

    def setUp(self) -> None:
        self.fields = {
            "title": "Test Problem",
            "link": "https://boj.kr/1000",
            "description": "테스트용 문제입니다.",
            "input_description": "입력이 없습니다.",
            "output_description": "출력이 없습니다.",
            "memory_limit": 0,
            "time_limit": 0,
        }
        self.client.force_login(self.user)

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
    maxDiff = None

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(**{
            User.field_name.USERNAME: "test",
            User.field_name.PASSWORD: "test",
            User.field_name.EMAIL: "test@example.com",
            User.field_name.BOJ_USERNAME: "test",
        })
        cls.problem = models.ProblemDAO.objects.create(**{
            models.ProblemDAO.field_name.TITLE: "Test Problem",
            models.ProblemDAO.field_name.LINK: "https://boj.kr/1000",
            models.ProblemDAO.field_name.DESCRIPTION: "테스트용 문제입니다.",
            models.ProblemDAO.field_name.INPUT_DESCRIPTION: "입력이 없습니다.",
            models.ProblemDAO.field_name.OUTPUT_DESCRIPTION: "출력이 없습니다.",
            models.ProblemDAO.field_name.MEMORY_LIMIT: 0,
            models.ProblemDAO.field_name.TIME_LIMIT: 0,
            models.ProblemDAO.field_name.CREATED_BY: cls.user,
        })
        cls.another_user = User.objects.create(**{
            User.field_name.USERNAME: "another",
            User.field_name.PASSWORD: "another",
            User.field_name.EMAIL: "another@example.com",
            User.field_name.BOJ_USERNAME: "another",
        })
        cls.another_problem = models.ProblemDAO.objects.create(**{
            models.ProblemDAO.field_name.TITLE: "Another Test Problem",
            models.ProblemDAO.field_name.LINK: "https://boj.kr/1001",
            models.ProblemDAO.field_name.DESCRIPTION: "또 다른 테스트용 문제입니다.",
            models.ProblemDAO.field_name.INPUT_DESCRIPTION: "입력이 없습니다.",
            models.ProblemDAO.field_name.OUTPUT_DESCRIPTION: "출력이 없습니다.",
            models.ProblemDAO.field_name.MEMORY_LIMIT: 0,
            models.ProblemDAO.field_name.TIME_LIMIT: 0,
            models.ProblemDAO.field_name.CREATED_BY: cls.another_user,
        })

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_200_내가_만든_문제(self):
        res = self.client.get(f"/api/v1/problem_ref/{self.problem.pk}")
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.json())

    def test_403_내가_만들지_않은_문제(self):
        res = self.client.get(f"/api/v1/problem_ref/{self.another_problem.pk}")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class ProblemSearchListAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(**{
            User.field_name.USERNAME: "test",
            User.field_name.PASSWORD: "test",
            User.field_name.EMAIL: "test@example.com",
            User.field_name.BOJ_USERNAME: "test",
        })
        cls.problem = models.ProblemDAO.objects.create(**{
            models.ProblemDAO.field_name.TITLE: "Test Problem",
            models.ProblemDAO.field_name.LINK: "https://boj.kr/1000",
            models.ProblemDAO.field_name.DESCRIPTION: "테스트용 문제입니다.",
            models.ProblemDAO.field_name.INPUT_DESCRIPTION: "입력이 없습니다.",
            models.ProblemDAO.field_name.OUTPUT_DESCRIPTION: "출력이 없습니다.",
            models.ProblemDAO.field_name.MEMORY_LIMIT: 0,
            models.ProblemDAO.field_name.TIME_LIMIT: 0,
            models.ProblemDAO.field_name.CREATED_BY: cls.user,
        })
        cls.another_user = User.objects.create(**{
            User.field_name.USERNAME: "another",
            User.field_name.PASSWORD: "another",
            User.field_name.EMAIL: "another@example.com",
            User.field_name.BOJ_USERNAME: "another",
        })
        cls.another_problem = models.ProblemDAO.objects.create(**{
            models.ProblemDAO.field_name.TITLE: "Another Test Problem",
            models.ProblemDAO.field_name.LINK: "https://boj.kr/1001",
            models.ProblemDAO.field_name.DESCRIPTION: "또 다른 테스트용 문제입니다.",
            models.ProblemDAO.field_name.INPUT_DESCRIPTION: "입력이 없습니다.",
            models.ProblemDAO.field_name.OUTPUT_DESCRIPTION: "출력이 없습니다.",
            models.ProblemDAO.field_name.MEMORY_LIMIT: 0,
            models.ProblemDAO.field_name.TIME_LIMIT: 0,
            models.ProblemDAO.field_name.CREATED_BY: cls.another_user,
        })

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_200_모든_문제_가져오기(self):
        res = self.client.get("/api/v1/problem_refs")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['title'], self.problem.title)
