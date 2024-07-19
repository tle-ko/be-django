from django.db import models


RANK_NAMES = {
    'ko': {
        0: '난이도를 매길 수 없음',
        1: '브론즈',
        2: '실버',
        3: '골드',
        4: '플래티넘',
        5: '다이아몬드',
        6: '루비',
    },
    'en': {
        0: 'Unrated',
        1: 'Bronze',
        2: 'Silver',
        3: 'Gold',
        4: 'Platinum',
        5: 'Diamond',
        6: 'Ruby',
    },
}

ARABIC_NUMERALS = {
    0: '',
    1: 'I',
    2: 'II',
    3: 'III',
    4: 'IV',
    5: 'V',
}


class UserSolvedTier(models.IntegerChoices):
    U = 0, 'Unrated'
    B5 = 1, '브론즈 5'
    B4 = 2, '브론즈 4'
    B3 = 3, '브론즈 3'
    B2 = 4, '브론즈 2'
    B1 = 5, '브론즈 1'
    S5 = 6, '실버 5'
    S4 = 7, '실버 4'
    S3 = 8, '실버 3'
    S2 = 9, '실버 2'
    S1 = 10, '실버 1'
    G5 = 11, '골드 5'
    G4 = 12, '골드 4'
    G3 = 13, '골드 3'
    G2 = 14, '골드 2'
    G1 = 15, '골드 1'
    P5 = 16, '플래티넘 5'
    P4 = 17, '플래티넘 4'
    P3 = 18, '플래티넘 3'
    P2 = 19, '플래티넘 2'
    P1 = 20, '플래티넘 1'
    D5 = 21, '다이아몬드 5'
    D4 = 22, '다이아몬드 4'
    D3 = 23, '다이아몬드 3'
    D2 = 24, '다이아몬드 2'
    D1 = 25, '다이아몬드 1'
    R5 = 26, '루비 5'
    R4 = 27, '루비 4'
    R3 = 28, '루비 3'
    R2 = 29, '루비 2'
    R1 = 30, '루비 1'

    @classmethod
    def get_rank(cls, value: int) -> int:
        if value == 0:
            return 0
        assert 1 <= value <= 30
        return ((value-1) // 5)+1

    @classmethod
    def get_rank_name(cls, value: int, lang='en') -> str:
        assert 0 <= value <= 30
        return RANK_NAMES[lang][cls.get_rank(value)]

    @classmethod
    def get_tier(cls, value: int) -> int:
        if value == 0:
            return 0
        assert 1 <= value <= 30
        return 5 - ((value-1) % 5)

    @classmethod
    def get_tier_name(cls, value: int, arabic=True) -> str:
        assert 0 <= value <= 30
        tier = cls.get_tier(value)
        if arabic:
            return ARABIC_NUMERALS[tier]
        return str(tier)

    @classmethod
    def get_name(cls, value: int, lang='en', arabic=True) -> str:
        assert 0 <= value <= 30
        return f'{cls.get_rank_name(value, lang=lang)} {cls.get_tier_name(value, arabic=arabic)}'
