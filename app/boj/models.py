from django.db import models

from core.models import Tag
from user.models import User


class BOJLevel(models.IntegerChoices):
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


class BOJUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='boj_user',
        help_text=(
            '이 사용자와 연결된 사용자를 입력해주세요.'
        ),
    )
    boj_id = models.CharField(
        max_length=100, # TODO: 추후 최대 아이디 길이 조사 필요
        help_text=(
            '백준 아이디를 입력해주세요.'
        ),
        unique=True,
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=(
            '이 사용자가 백준 사용자임을 확인했는지 여부를 입력해주세요.'
        ),
    )
    level = models.IntegerField(
        help_text=(
            '백준 레벨을 입력해주세요.'
        ),
        choices=BOJLevel.choices,
        default=BOJLevel.U,
    )
    updated_at = models.DateTimeField(
        help_text=(
            '이 사용자의 정보가 최근에 업데이트된 시간을 입력해주세요.'
        ),
        auto_now=True,
    )

    def __repr__(self) -> str:
        return f'[@{self.boj_id} | *{BOJLevel(self.level).label}]'

    def __str__(self) -> str:
        verified = 'verified' if self.is_verified else 'not-verified'
        return f'{self.pk} : {self.user.__repr__()} ← {self.__repr__()} ({verified})'


class BOJTag(models.Model):
    tag = models.OneToOneField(
        Tag,
        on_delete=models.CASCADE,
        related_name='boj_tag',
        help_text=(
            '이 태그와 연결된 알고리즘 태그를 입력해주세요.'
        ),
    )
    boj_id = models.IntegerField(
        unique=True,
        help_text=(
            '백준 태그 ID를 입력해주세요.'
        ),
        null=True,
        default=None,
    )

    def __str__(self) -> str:
        return f'{self.boj_id} : {self.tag.__repr__()}'
