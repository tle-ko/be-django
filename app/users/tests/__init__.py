from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from users.models import User, BojLevelChoices


class SignInTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.url = '/api/v1/auth/signin'
        self.now = timezone.now()
        self.user = User.objects.create(**{
            User.field_name.EMAIL: 'email@example.com',
            User.field_name.USERNAME: 'username',
            User.field_name.PASSWORD: 'password',
            User.field_name.BOJ_USERNAME: 'boj_username',
            User.field_name.BOJ_LEVEL: BojLevelChoices.S1,
            User.field_name.BOJ_LEVEL_UPDATED_AT: self.now,
        })

    def test_returns_200(self):
        res = self.client.post(self.url, {
            'email': 'email@example.com',
            'password': 'password',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_returns_400(self):
        res = self.client.post(self.url, {
            'username': 'username',
            'password': 'password',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_403(self):
        res = self.client.post(self.url, {
            'email': 'email@example.com',
            'password': 'password2',
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_200_response(self):
        res = self.client.post(self.url, {
            'email': 'email@example.com',
            'password': 'password',
        })
        user = User.objects.get(pk=1)
        self.assertJSONEqual(res.content, {
            'id': 1,
            'boj': {
                'username': 'boj_username',
                'profile_url': 'https://boj.kr/boj_username',
                'level': 10,
                'division': 2,
                'division_name_en': 'Silver',
                'division_name_ko': '실버',
                'tier': 1,
                'tier_name': 'I',
                'tier_updated_at': user.boj_level_updated_at.isoformat(),
            },
            'profile_image': None,
            'username': 'username',
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat(),
        })
