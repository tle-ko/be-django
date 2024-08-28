from logging import getLogger

from background_task import background
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import requests

from boj.models import BOJUser
from boj.models import BOJUserSnapshot
from users.models import User


logger = getLogger('django.server')


@receiver(post_save, sender=User)
def auto_create_boj_user(sender, instance: User, created: bool, **kwargs):
    update_boj_user_data(instance.username)


@receiver(post_save, sender=BOJUser)
def auto_update_boj_user(sender, instance: BOJUser, created: bool, **kwargs):
    if created:
        update_boj_user_data(instance.username)


@background
def update_boj_user_data(username: str):
    instance = BOJUser.objects.get_by_username(username)
    url = f'https://solved.ac/api/v3/user/show?handle={username}'
    data = requests.get(url).json()
    try:
        instance.level = data['tier']
        instance.rating = data['rating']
        instance.updated_at = timezone.now()
        instance.save()
        BOJUserSnapshot.objects.create_snapshot_of(instance)
    except AssertionError:
        # Solved.ac API 관련 문제일 가능성이 높다.
        logger.warning(f'"{url}"로 부터 데이터를 파싱해오는 것에 실패했습니다.')
