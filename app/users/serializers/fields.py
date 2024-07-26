from users.models import User, UserBojLevel
from users.serializers.mixins import ReadOnlyField


class UserBojField(ReadOnlyField):
    def to_representation(self, user: User):
        if user.boj_username is None:
            user_boj_level = UserBojLevel.U
        else:
            user_boj_level = UserBojLevel(user.boj_level)
        return {
            'username': user.boj_username,
            'profile_url': f'https://boj.kr/{user.boj_username}',
            'level': user_boj_level.value,
            'division': user_boj_level.get_division(),
            'division_name_en': user_boj_level.get_division_name(lang='en'),
            'division_name_ko': user_boj_level.get_division_name(lang='ko'),
            'tier': user_boj_level.get_tier(),
            'tier_name': user_boj_level.get_tier_name(arabic=True),
            'tier_updated_at': user.boj_level_updated_at,
        }
