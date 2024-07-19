from rest_framework.serializers import Serializer

from tle.models import User
from tle.models.choices import UserSolvedTier


class BojProfileMixin:
    def boj_profile(self: Serializer, user: User) -> dict:
        return {
            'username': user.boj_username,
            'profile_url': f'https://boj.kr/{user.boj_username}',
            'level': user.boj_tier,
            'rank': UserSolvedTier.get_rank(user.boj_tier),
            'rank_name_en': UserSolvedTier.get_rank_name(user.boj_tier, lang='en'),
            'rank_name_ko': UserSolvedTier.get_rank_name(user.boj_tier, lang='ko'),
            'tier': UserSolvedTier.get_tier(user.boj_tier),
            'tier_name': UserSolvedTier.get_tier_name(user.boj_tier, arabic=True),
            'tier_updated_at': user.boj_tier_updated_at,
        }
