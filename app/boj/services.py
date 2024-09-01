from json import JSONDecodeError
from logging import getLogger

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework import status
import requests

from background_task.tasks import tasks
from boj.models import BOJUser
from boj.models import BOJUserSnapshot
from users.models import User


logger = getLogger(__name__)


@receiver(post_save, sender=User)
def auto_create_boj_user(sender, instance: User, created: bool, **kwargs):
    schedule_update_boj_user_data(instance.username)


@receiver(post_save, sender=BOJUser)
def auto_update_boj_user(sender, instance: BOJUser, created: bool, **kwargs):
    if created:
        schedule_update_boj_user_data(instance.username)


def schedule_update_boj_user_data(username: str):
    assert username.strip().isidentifier()
    _update_boj_user_data(username)


@tasks.background
def _update_boj_user_data(username: str):
    assert username.strip().isidentifier()
    instance = BOJUser.objects.get_by_username(username)
    url = f'https://solved.ac/api/v3/user/show?handle={username}'
    res = requests.get(url)
    if res.status_code == status.HTTP_404_NOT_FOUND:
        logger.info(f'사용자 명이 "{username}"인 사용자가 존재하지 않습니다.')
    else:
        try:
            data = res.json()
            instance.level = data['tier']
            instance.rating = data['rating']
            instance.updated_at = timezone.now()
            instance.save()
            BOJUserSnapshot.objects.create_snapshot_of(instance)
        except AssertionError:
            # Solved.ac API 관련 문제일 가능성이 높다.
            logger.warning(f'"{url}"로 부터 데이터를 파싱해오는 것에 실패했습니다.')
        except JSONDecodeError:
            logger.warning(f'"{url}"로 부터 데이터를 파싱해오는 것에 실패했습니다.')
            logger.error(f'받은 데이터: "{res.content}"')
