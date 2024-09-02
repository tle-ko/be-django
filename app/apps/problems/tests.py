from django.test import TestCase
from rest_framework import status

from users.models import User


class ProblemCreateAPIViewTest(TestCase):
    fixtures = ['sample.json']
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.sample_data = {
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
        res = self.client.post("/api/v1/problem", self.sample_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_401_비로그인_사용_불가(self):
        self.client.logout()
        res = self.client.post("/api/v1/problem", self.sample_data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_201_링크가_누락_되어도_문제_생성_가능(self):
        data = self.sample_data.copy()
        del data['link']
        res = self.client.post("/api/v1/problem", data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_400_일부_필드_누락(self):
        for drop_field in self.required_fields:
            with self.subTest(drop_field=drop_field):
                res = self.client.post("/api/v1/problem", {
                    field: self.sample_data[field]
                    for field in self.required_fields if field != drop_field
                })
                self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
