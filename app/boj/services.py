from __future__ import annotations

import logging

from background_task import background
from django.utils import timezone
import requests

from boj import dto
from boj import enums
from boj import models


logger = logging.getLogger('tle.boj')


def get_boj_user_service(boj_username: str) -> BOJUserService:
    return BOJUserService(boj_username)


class BOJUserService:
    def __init__(self, username: str):
        self.username = username
        self.instance, created = models.BOJUser.objects.get_or_create(**{
            models.BOJUser.field_name.USERNAME: username,
        })

    def update(self) -> None:
        update_boj_user(self.username)

    def create_snapshot(self) -> models.BOJUserSnapshot:
        return models.BOJUserSnapshot(**{
            models.BOJUserSnapshot.field_name.USER: self.instance,
            models.BOJUserSnapshot.field_name.LEVEL: self.instance.level,
            models.BOJUserSnapshot.field_name.RATING: self.instance.rating,
            models.BOJUserSnapshot.field_name.CREATED_AT: self.instance.updated_at,
        })

    def level(self) -> enums.BOJLevel:
        return enums.BOJLevel(self.instance.level)


@background
def update_boj_user(boj_username: str):
    data = fetch_data(boj_username)
    service = get_boj_user_service(boj_username)
    service.instance.level = data.level.value
    service.instance.rating = data.rating
    service.instance.updated_at = timezone.now()
    service.instance.save()
    service.create_snapshot()


def fetch_data(username: str) -> dto.BOJUserData:
    url = f'https://solved.ac/api/v3/user/show?handle={username}'
    data = requests.get(url).json()
    try:
        tier = data['tier']
        rating = data['rating']
    except AssertionError:
        # Solved.ac API 관련 문제일 가능성이 높다.
        logger.warning(
            '"https://solved.ac/api/v3/user/show"로 부터 데이터를 파싱해오는 것에 실패했습니다.'
        )
    else:
        return dto.BOJUserData(level=enums.BOJLevel(tier), rating=rating)
