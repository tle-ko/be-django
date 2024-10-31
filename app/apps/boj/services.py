import json
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework import status
import requests

from apps.background_task import background
from users.models import User

from . import enums
from . import models


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def post_save_user(sender, instance: User, created: bool, **kwargs):
    fields = {models.BOJUserDAO.field_name.USERNAME: instance.boj_username}
    if not models.BOJUserDAO.objects.filter(**fields).exists():
        models.BOJUserDAO.objects.create(**fields)


@receiver(post_save, sender=models.BOJUserDAO)
def post_save_boj_user(sender, instance: models.BOJUserDAO, created: bool, **kwargs):
    # 새로운 BOJUser가 등록되면 자동으로 정보를 불러온다.
    if created:
        schedule_update_boj_user_data(instance.username)
    else:
        models.BOJUserSnapshotDAO.objects.create(**{
            models.BOJUserSnapshotDAO.field_name.USER: instance,
            models.BOJUserSnapshotDAO.field_name.LEVEL: instance.level,
            models.BOJUserSnapshotDAO.field_name.RATING: instance.rating,
            models.BOJUserSnapshotDAO.field_name.CREATED_AT: instance.updated_at,
        })


@background
def regular_update_boj_user_data():
    for instance in models.BOJUserDAO.objects.all():
        schedule_update_boj_user_data(instance.username)


@background
def schedule_update_boj_user_data(username: str):
    if not username.strip().isidentifier():
        logger.warning(f'BOJ username "{username}" is invalid.')
        return
    update_boj_user_data(username)


def update_boj_user_data(username: str):
    raw_boj_user_data = _fetch_boj_user_data(username)
    instance = models.BOJUserDAO.objects.get(**{
        models.BOJUserDAO.field_name.USERNAME: username,
    })
    instance.level = raw_boj_user_data['tier']
    instance.rating = raw_boj_user_data['rating']
    instance.updated_at = timezone.now()
    instance.save()


def _fetch_boj_user_data(username: str) -> dict:
    url = f'https://solved.ac/api/v3/user/show?handle={username}'
    res = requests.get(url)
    if res.status_code == status.HTTP_404_NOT_FOUND:
        logger.info(f'사용자 명이 "{username}"인 사용자가 존재하지 않습니다.')
    try:
        data = res.json()
        assert 'tier' in data
        assert 'rating' in data
    except (AssertionError, json.JSONDecodeError):
        # Solved.ac API 관련 문제일 가능성이 높다.
        logger.warning(f'"{url}"로 부터 데이터를 파싱해오는 것에 실패했습니다.')
        logger.error(f'받은 데이터: "{res.content}"')
        data = {
            'tier': enums.BOJLevel.U,
            'rating': 0,
        }
    finally:
        return data
