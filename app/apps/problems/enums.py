from __future__ import annotations

from django.db import models


class Unit(models.TextChoices):
    MEGA_BYTE = 'MB', "메가 바이트"
    SECOND = 's', "초"


NAMES = {
    'ko': ['분석 중', '쉬움', '보통', '어려움'],
    'en': ['UNDER ANALYSIS', 'EASY', 'NORMAL', 'HARD'],
}


class ProblemDifficulty(models.IntegerChoices):
    @staticmethod
    def from_label(label: str) -> ProblemDifficulty:
        return {
            'EASY': ProblemDifficulty.EASY,
            'NORMAL': ProblemDifficulty.NORMAL,
            'HARD': ProblemDifficulty.HARD,
        }[label]

    UNDER_ANALYSIS = 0, '분석 중'
    EASY = 1, '쉬움'
    NORMAL = 2, '보통'
    HARD = 3, '어려움'

    def get_name(self, lang='ko') -> str:
        if lang not in NAMES:
            raise ValueError(
                f'Invalid language: {lang}, ',
                f'choose from {NAMES.keys()}'
            )
        return NAMES[lang][self.value]
