from django.db import models


NAMES = {
    'ko': {
        1: '쉬움',
        2: '보통',
        3: '어려움',
    },
    'en': {
        1: 'EASY',
        2: 'NORMAL',
        3: 'HARD',
    },
}


class ProblemDifficulty(models.IntegerChoices):
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
