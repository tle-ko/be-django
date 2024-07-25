from rest_framework.serializers import Serializer

from tle.models import User
from tle.models.choices import BojUserLevel


class BojProfileMixin:
    def boj_profile(self: Serializer, user: User) -> dict:
        return {
            'username': user.boj_username,
            'profile_url': f'https://boj.kr/{user.boj_username}',
            'level': user.boj_level,
            'division': BojUserLevel.get_division(user.boj_level),
            'division_name_en': BojUserLevel.get_division_name(user.boj_level, lang='en'),
            'division_name_ko': BojUserLevel.get_division_name(user.boj_level, lang='ko'),
            'tier': BojUserLevel.get_tier(user.boj_level),
            'tier_name': BojUserLevel.get_tier_name(user.boj_level, arabic=True),
            'tier_updated_at': user.boj_level_updated_at,
        }
