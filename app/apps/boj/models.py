from __future__ import annotations

from datetime import timedelta
from json import JSONDecodeError
from logging import getLogger

from django.db.models import Manager
from django.dispatch import receiver
from django.utils import timezone
from rest_framework import status
import requests

from apps.background_task import background
from users.models import User

from . import db
from . import dto
from . import enums
from . import signals


logger = getLogger(__name__)


class BOJUserManager(Manager):
    def create(self, username: str) -> BOJUser:
        kwargs = {}
        kwargs[BOJUser.field_name.USERNAME] = username
        return super().create(**kwargs)

    def get(self, username: str) -> BOJUser:
        kwargs = {}
        kwargs[BOJUser.field_name.USERNAME] = username
        return super().get(**kwargs)

    def get_or_create(self, username: str) -> BOJUser:
        kwargs = {}
        kwargs[BOJUser.field_name.USERNAME] = username
        return super().get_or_create(**kwargs)[0]

    def exists(self, username: str) -> bool:
        kwargs = {}
        kwargs[BOJUser.field_name.USERNAME] = username
        return self.filter(**kwargs).exists()


class BOJUser(db.BOJUserDAO):
    objects: BOJUserManager = BOJUserManager()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.BOJUserDTO:
        return dto.BOJUserDTO(
            username = self.username,
            profile_url = f'https://boj.kr/{self.username}',
            level = dto.BOJLevelDTO(self.level),
            rating = self.rating,
            updated_at = self.updated_at,
        )

    def create_snapshot(self) -> BOJUserSnapshot:
        return BOJUserSnapshot.objects.create(**{
            BOJUserSnapshot.field_name.USER: self,
            BOJUserSnapshot.field_name.LEVEL: self.level,
            BOJUserSnapshot.field_name.RATING: self.rating,
            BOJUserSnapshot.field_name.CREATED_AT: self.updated_at,
        })

    def update(self):
        raw_boj_user_data = fetch_boj_user_data(self.username)
        self.level = raw_boj_user_data['tier']
        self.rating = raw_boj_user_data['rating']
        self.updated_at = timezone.now()
        self.save()
        self.create_snapshot()

    def schedule_update(self):
        schedule_update_boj_user_data(self.username)


class BOJUserSnapshot(db.BOJUserSnapshotDAO):
    class Meta:
        proxy = True


@receiver(signals.post_save, sender=User)
def auto_create_boj_user(sender, instance: User, created: bool, **kwargs):
    if not BOJUser.objects.exists(instance.boj_username):
        BOJUser.objects.get_or_create(instance.boj_username)


@receiver(signals.post_save, sender=BOJUser)
def on_boj_user_created(sender, instance: BOJUser, created: bool, **kwargs):
    # 새로운 BOJUser가 등록되면 자동으로 정보를 불러온다.
    if created:
        schedule_update_boj_user_data(instance.username)


@background
def schedule_update_boj_user_data(username: str):
    assert username.strip().isidentifier()
    instance = BOJUser.objects.get(username)
    # 마지막 갱신으로 부터 90초 이내에 시도한 갱신 요청은 무시 함.
    if (timezone.now() - instance.updated_at) < timedelta(seconds=90):
        logger.info(f'백준 사용자 "{username}"의 정보 갱신 요청이 무시됨. (사유: 너무 잦은 갱신 요청)')
        return
    instance.update()


def fetch_boj_user_data(username: str) -> dict:
    url = f'https://solved.ac/api/v3/user/show?handle={username}'
    res = requests.get(url)
    if res.status_code == status.HTTP_404_NOT_FOUND:
        logger.info(f'사용자 명이 "{username}"인 사용자가 존재하지 않습니다.')
    try:
        data = res.json()
        assert 'tier' in data
        assert 'rating' in data
    except (AssertionError, JSONDecodeError):
        # Solved.ac API 관련 문제일 가능성이 높다.
        logger.warning(f'"{url}"로 부터 데이터를 파싱해오는 것에 실패했습니다.')
        logger.error(f'받은 데이터: "{res.content}"')
        data = {
            'tier': enums.BOJLevel.U,
            'rating': 0,
        }
    finally:
        return data
