from django.db import models


NAMES = {
    'ko': ['분석 중', '쉬움', '보통', '어려움'],
    'en': ['UNDER ANALYSIS', 'EASY', 'NORMAL', 'HARD'],
}


class ProblemDifficulty(models.IntegerChoices):
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
