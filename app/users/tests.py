from django.test import TestCase
from rest_framework import status

from users.models import User
from users.models import UserEmailVerification


class SignInTest(TestCase):
    fixtures = ['user.sample.json']

    def setUp(self) -> None:
        self.client.logout()

    def test_200_로그인성공(self):
        res = self.client.post("/api/v1/auth/signin", {
            "email": "test@example.com",
            "password": "passw0rd@test",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        token = data.pop('token')
        self.assertGreater(len(token), 1)
        self.assertDictEqual(data, {
            "id": 1,
            "username": "test",
            "profile_image": None,
            "refresh_token": None,
            "boj": {
                "username": "test",
                "profile_url": "https://boj.kr/test",
                "level": {
                    "value": 0,
                    "name": "사용자 정보를 불러오지 못함",
                },
                "rating": 0,
                "updated_at": "2024-08-27T04:02:23.327000",
            },
        })

    def test_403_비밀번호_불일치(self):
        res = self.client.post("/api/v1/auth/signin", {
            "email": "test@example.com",
            "password": "password@test",
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class SignUpTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.sample_object = UserEmailVerification.objects.create(**{
            UserEmailVerification.field_name.EMAIL: "test@example.com",
            UserEmailVerification.field_name.VERIFICATION_TOKEN: 'sample_token',
        })

    def test_201_회원가입_성공(self):
        res = self.client.post("/api/v1/auth/signup", {
            "email": self.sample_object.email,
            "username": "test",
            "password": "passw0rd@test",
            "boj_username": "test",
            "verification_token": self.sample_object.verification_token,
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_400_인증토큰_불일치(self):
        res = self.client.post("/api/v1/auth/signup", {
            "email": self.sample_object.email,
            "username": "test",
            "password": "passw0rd@test",
            "boj_username": "test",
            "verification_token": 'this_token_must_not_match_the_sample...',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class SignOutTest(TestCase):
    fixtures = ['user.sample.json']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_204_로그아웃_성공(self):
        res = self.client.get("/api/v1/auth/signout")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class UsabilityAPITest(TestCase):
    fixtures = ['user.sample.json']

    def test_200_사용_가능한_이메일(self):
        res = self.client.get("/api/v1/auth/usability", {
            "email": "unique@notexample.com",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.json(), {
            "email": {
                "value": "unique@notexample.com",
                "is_usable": True,
            },
            "username": {
                "value": None,
                "is_usable": False,
            },
        })

    def test_200_사용_불가능한_이메일(self):
        res = self.client.get("/api/v1/auth/usability", {
            "email": "test@example.com",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.json(), {
            "email": {
                "value": "test@example.com",
                "is_usable": False,
            },
            "username": {
                "value": None,
                "is_usable": False,
            },
        })

    def test_200_사용_가능한_사용자명(self):
        res = self.client.get("/api/v1/auth/usability", {
            "username": "unique",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.json(), {
            "email": {
                "value": None,
                "is_usable": False,
            },
            "username": {
                "value": "unique",
                "is_usable": True,
            },
        })

    def test_200_사용_불가능한_사용자명(self):
        res = self.client.get("/api/v1/auth/usability", {
            "username": "test",
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.json(), {
            "email": {
                "value": None,
                "is_usable": False,
            },
            "username": {
                "value": "test",
                "is_usable": False,
            },
        })

    def test_400_빈_데이터_전송(self):
        res = self.client.get("/api/v1/auth/usability")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class UserManageAPITest(TestCase):
    fixtures = ['user.sample.json']

    def setUp(self) -> None:
        self.client.force_login(user=User.objects.get(username='test'))

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

    def test_200_GET_정보_가져오기(self):
        res = self.client.get("/api/v1/user/manage")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.json(), {
            "email": "test@example.com",
            "profile_image": None,
            "username": "test",
            "boj": {
                "username": "test",
                "profile_url": "https://boj.kr/test",
                "level": {
                    "value": 0,
                    "name": "사용자 정보를 불러오지 못함",
                },
                "rating": 0,
                "updated_at": "2024-08-27T04:02:23.327000",
            }
        })

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
        self.assertDictEqual(res.json(), {
            "email": "test@example.com",
            "profile_image": None,
            "username": "alt_test",
            "boj": {
                "username": "test",
                "profile_url": "https://boj.kr/test",
                "level": {
                    "value": 0,
                    "name": "사용자 정보를 불러오지 못함",
                },
                "rating": 0,
                "updated_at": "2024-08-27T04:02:23.327000",
            }
        })

    def test_200_PATCH_비밀번호_수정하기(self):
        res = self.client.patch("/api/v1/user/manage", {
            "password": "passw0rd@new_password",
        }, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.json(), {
            "email": "test@example.com",
            "profile_image": None,
            "username": "test",
            "boj": {
                "username": "test",
                "profile_url": "https://boj.kr/test",
                "level": {
                    "value": 0,
                    "name": "사용자 정보를 불러오지 못함",
                },
                "rating": 0,
                "updated_at": "2024-08-27T04:02:23.327000",
            }
        })
        user = User.objects.filter(username='test').get()
        self.assertTrue(user.check_password("passw0rd@new_password"))
