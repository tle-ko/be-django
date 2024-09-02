from json import JSONDecodeError
from logging import getLogger
from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework import status
import requests

from apps.background_task.tasks import tasks
from apps.boj.enums import BOJLevel
from apps.boj.models import BOJUser
from apps.boj.models import BOJUserSnapshot
from users.models import User


logger = getLogger(__name__)


@receiver(post_save, sender=User)
def auto_create_boj_user(sender, instance: User, created: bool, **kwargs):
    schedule_update_boj_user_data(instance.boj_username)


@tasks.background
def schedule_update_boj_user_data(username: str):
    assert username.strip().isidentifier()
    instance, created = BOJUser.objects.get_or_create_by_username(username)

    # 마지막 갱신으로 부터 90초 이내에 시도한 갱신 요청은 무시 함.
    if not created and (timezone.now() - instance.updated_at) < timedelta(seconds=90):
        logger.info(f'백준 사용자 "{username}"의 정보 갱신 요청이 무시됨. (사유: 너무 잦은 갱신 요청)')
        return

    update_boj_user(instance)


def update_boj_user(instance: BOJUser):
    raw_boj_user_data = fetch_boj_user_data(instance.username)
    instance.level = raw_boj_user_data['tier']
    instance.rating = raw_boj_user_data['rating']
    instance.updated_at = timezone.now()
    instance.save()
    BOJUserSnapshot.objects.create_snapshot_of(instance)


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
            'tier': BOJLevel.U,
            'rating': 0,
        }
    finally:
        return data
