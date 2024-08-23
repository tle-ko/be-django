import logging

from django.utils import timezone
import background_task
import requests

from boj import dto
from boj import enums
from boj import models


logger = logging.getLogger('tle.boj')


def get_object(username: str) -> models.BOJUser:
    obj, created = models.BOJUser.objects.get_or_create(**{
        models.BOJUser.field_name.USERNAME: username,
    })
    return obj


def snapshot(obj: models.BOJUser) -> models.BOJUserSnapshot:
    return models.BOJUserSnapshot(**{
        models.BOJUserSnapshot.field_name.USER: obj,
        models.BOJUserSnapshot.field_name.LEVEL: obj.level,
        models.BOJUserSnapshot.field_name.RATING: obj.rating,
        models.BOJUserSnapshot.field_name.CREATED_AT: obj.updated_at,
    })


@background_task.background()
def fetch(username: str) -> None:
    data = fetch_data(username)
    obj = get_object(username)
    obj.level = data.level.value
    obj.rating = data.rating
    obj.updated_at = timezone.now()
    obj.save()
    snapshot(obj).save()


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
