from django.test import TestCase
from rest_framework import status

from . import models


class SignInTest(TestCase):
    fixtures = ['tests/users.json']

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Check fixtures
        user: models.User = models.User.objects.get(pk=1)
        assert user.email == 'test@example.com'
        assert user.check_password('passw0rd@test')

    def setUp(self) -> None:
        self.client.logout()

    def test_200_세션_로그인성공(self):
        res = self.client.post("/api/v1/auth/signin", {
            "email": "test@example.com",
            "password": "passw0rd@test",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_200_세션_로그인에_토큰_포함(self):
        res = self.client.post("/api/v1/auth/signin", {
            "email": "test@example.com",
            "password": "passw0rd@test",
        })
        self.assertIn('token', res.json())

    def test_403_비밀번호_불일치(self):
        res = self.client.post("/api/v1/auth/signin", {
            "email": "test@example.com",
            "password": "password@test",
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_200_Bearer_토큰_로그인(self):
        # 인증 토큰 발급받기
        res = self.client.post("/api/v1/auth/signin", {
            "email": "test@example.com",
            "password": "passw0rd@test",
        })
        token = res.json()['token']

        # 임의로 로그인이 필요한 기능 사용 (로그아웃 됨을 확인)
        self.client.logout()
        res = self.client.get("/api/v1/user/manage")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # 임의로 로그인이 필요한 기능 사용 (토큰 로그인 시도)
        res = self.client.get("/api/v1/user/manage", headers={
            'Authorization': f'Bearer {token}',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class SignUpTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.fields = {
            models.UserEmailVerification.field_name.EMAIL: "test@example.com",
            models.UserEmailVerification.field_name.VERIFICATION_TOKEN: 'sample_token',
        }
        models.UserEmailVerification.objects.create(**cls.fields)

    def test_201_회원가입_성공(self):
        res = self.client.post("/api/v1/auth/signup", {
            "email": "test@example.com",
            "username": "test",
            "password": "passw0rd@test",
            "boj_username": "test",
            "verification_token": "sample_token",
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_400_인증토큰_불일치(self):
        res = self.client.post("/api/v1/auth/signup", {
            "email": "test@example.com",
            "username": "test",
            "password": "passw0rd@test",
            "boj_username": "test",
            "verification_token": 'this_token_must_not_match_the_sample...',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class SignOutTest(TestCase):
    fixtures = ['tests/users.json']

    def setUp(self) -> None:
        self.user = models.User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_204_로그아웃_성공(self):
        res = self.client.get("/api/v1/auth/signout")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class UsabilityAPITest(TestCase):
    fixtures = ['tests/users.json']

    def test_400_빈_데이터_전송(self):
        res = self.client.get("/api/v1/auth/usability")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_200_사용_가능한_이메일(self):
        res = self.client.get("/api/v1/auth/usability", {
            "email": "unique@notexample.com",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()['email']['is_usable'])

    def test_200_사용_불가능한_이메일(self):
        res = self.client.get("/api/v1/auth/usability", {
            "email": "test@example.com",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(res.json()['email']['is_usable'])

    def test_200_사용_가능한_사용자명(self):
        res = self.client.get("/api/v1/auth/usability", {
            "username": "unique",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()['username']['is_usable'])

    def test_200_사용_불가능한_사용자명(self):
        res = self.client.get("/api/v1/auth/usability", {
            "username": "test",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(res.json()['username']['is_usable'])


class UserManageAPITest(TestCase):
    fixtures = ['tests/users.json']

    def setUp(self) -> None:
        self.client.force_login(self.get_user())

    def get_user(self) -> models.User:
        return models.User.objects.get(username='test')

    # 권한 테스트

    def test_401_GET_비로그인_사용자는_접근_불가(self):
        self.client.logout()
        res = self.client.get("/api/v1/user/manage")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_401_PUT_비로그인_사용자는_접근_불가(self):
        self.client.logout()
        res = self.client.put("/api/v1/user/manage")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_401_PATCT_비로그인_사용자는_접근_불가(self):
        self.client.logout()
        res = self.client.patch("/api/v1/user/manage")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # 기능 테스트

    def test_200_GET_정보_가져오기(self):
        res = self.client.get("/api/v1/user/manage")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_400_PATCH_이메일_수정하기(self):
        res = self.client.patch("/api/v1/user/manage", {
            "email": "test@example.com",
        }, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_200_PATCH_사용자명_수정하기(self):
        res = self.client.patch("/api/v1/user/manage", {
            "username": "alt_test",
        }, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['username'], 'alt_test')
        self.assertEqual(self.get_user().username, 'alt_test')

    def test_200_PATCH_비밀번호_수정하기(self):
        res = self.client.patch("/api/v1/user/manage", {
            "password": "passw0rd@new_password",
        }, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.get_user().check_password("passw0rd@new_password"))
