from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from crews.models import Crew
from users.models import User, BojLevelChoices


class CrewRecruitingTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.url = '/api/v1/crews/recruiting'
        self.user = User.objects.create(**{
            User.field_name.EMAIL: 'email@example.com',
            User.field_name.USERNAME: 'username',
            User.field_name.PASSWORD: 'password',
            User.field_name.BOJ_USERNAME: 'boj_username',
            User.field_name.BOJ_LEVEL: BojLevelChoices.S1,
        })
        self.crew = Crew.objects.create(**{
            Crew.field_name.NAME: '크루명',
            Crew.field_name.ICON: '😀',
            Crew.field_name.MAX_MEMBERS: 4,
            Crew.field_name.NOTICE: '공지',
            Crew.field_name.CUSTOM_TAGS: ["태그1", "태그2",],
            Crew.field_name.MIN_BOJ_LEVEL: BojLevelChoices.G5,
            Crew.field_name.IS_RECRUITING: True,
            Crew.field_name.IS_ACTIVE: True,
            Crew.field_name.CREATED_BY: self.user,
        })

    def test_returns_200(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_200_response(self):
        res = self.client.get(self.url)
        self.assertJSONEqual(res.content, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.crew.pk,
                    'icon': self.crew.icon,
                    'name': self.crew.name,
                    'is_active': self.crew.is_active,
                    'is_member': False,
                    'is_recruiting': self.crew.is_recruiting,
                    'is_joinable': False,
                    'activities': {
                        'count': 0,
                        'recent': {
                            'nth': None,
                            'name': '등록된 활동 없음',
                            'start_at': None,
                            'end_at': None,
                            'is_open': False,
                        }
                    },
                    'members': {
                        'count': 1,
                        'max_count': self.crew.max_members,
                        'items': [],
                    },
                    'tags': {
                        'count': 3,
                        'items': [
                            {
                                'key': None,
                                'name': '골드 5 이상',
                                'type': 'level',
                            },
                            {
                                'key': None,
                                'name': '태그1',
                                'type': 'custom',
                            },
                            {
                                'key': None,
                                'name': '태그2',
                                'type': 'custom',
                            },
                        ]
                    },
                }
            ],
        })
