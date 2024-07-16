from django.db import models


class ProblemDifficulty(models.IntegerChoices):
    EASY = 1, '쉬움'
    NORMAL = 2, '보통'
    HARD = 3, '어려움'
