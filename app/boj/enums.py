from django.db.models import IntegerChoices


DIVISION_NAMES = {
    'ko': ['난이도를 매길 수 없음', '브론즈', '실버', '골드', '플래티넘', '다이아몬드', '루비'],
    'en': ['Unrated', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Ruby'],
}
ARABIC_NUMERALS = ['', 'I', 'II', 'III', 'IV', 'V']


class BOJLevel(IntegerChoices):
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
    M = 31, '마스터'

    def get_division(self) -> int:
        if self == self.U:
            return 0
        return ((self.value-1) // 5)+1

    def get_division_name(self, lang='en') -> str:
        return DIVISION_NAMES[lang][self.get_division()]

    def get_tier(self) -> int:
        if self == self.U:
            return 0
        return 5 - ((self.value-1) % 5)

    def get_tier_name(self, arabic=True) -> str:
        tier = self.get_tier()
        if arabic:
            return ARABIC_NUMERALS[tier]
        return str(tier)

    def get_name(self, lang='en', arabic=True) -> str:
        if self.value == 0:
            return '사용자 정보를 불러오지 못함'
        return f'{self.get_division_name(lang=lang)} {self.get_tier_name(arabic=arabic)}'
