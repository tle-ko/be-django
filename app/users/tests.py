from django.test import TestCase
from rest_framework import status


class SignInTest(TestCase):
    fixtures = ['user.sample.json']

    def setUp(self) -> None:
        self.client.logout()

    def test_로그인성공(self):
        res = self.client.post(
            "/api/v1/auth/signin",
            {
                "email": "test@example.com",
                "password": "passw0rd@test",
            },
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_비밀번호_불일치(self):
        res = self.client.post(
            "/api/v1/auth/signin",
            {
                "email": "test@example.com",
                "password": "password@test",
            }
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
