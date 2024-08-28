from __future__ import annotations

from django.db import models


class Unit(models.TextChoices):
    MEGA_BYTE = 'MB', "메가 바이트"
    SECOND = 's', "초"
