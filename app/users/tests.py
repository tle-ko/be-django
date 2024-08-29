from django.test import TestCase
from rest_framework import status

from users.models import UserEmailVerification


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


class SignUpTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.sample_object = UserEmailVerification.objects.create(**{
            UserEmailVerification.field_name.EMAIL: "test@example.com",
            UserEmailVerification.field_name.VERIFICATION_TOKEN: 'sample_token',
        })

    def test_회원가입_성공(self):
        res = self.client.post(
            "/api/v1/auth/signup",
            {
                "email": self.sample_object.email,
                "username": "test",
                "password": "passw0rd@test",
                "boj_username": "test",
                "verification_token": self.sample_object.verification_token,
            }
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_인증토큰_불일치(self):
        res = self.client.post(
            "/api/v1/auth/signup",
            {
                "email": self.sample_object.email,
                "username": "test",
                "password": "passw0rd@test",
                "boj_username": "test",
                "verification_token": 'this_token_must_not_match_the_sample...',
            }
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class SignOutTest(TestCase):
    fixtures = ['user.sample.json']

    def setUp(self) -> None:
        # authenticate() 함수에서는 email을 username으로 바꾸어서 전달하기 때문에 아래와 같이 설정함.
        logged_in = self.client.login(**{
            "username": "test@example.com",
            "password": "passw0rd@test",
        })
        self.assertTrue(logged_in)

    def test_로그아웃_성공(self):
        res = self.client.get("/api/v1/auth/signout")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
