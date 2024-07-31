from __future__ import annotations
from datetime import timedelta
from hashlib import sha256
from random import randint

from django.db import models
from django.utils import timezone


N_CODES = 6

A, Z = ord('A'), ord('Z')


def default_verification_code_factory() -> str:
    def code(length=N_CODES):
        for _ in range(length):
            yield chr(randint(A, Z))
    return ''.join(code())


def default_verification_token_factory() -> str:
    return sha256(default_verification_code_factory()).hexdigest()


def default_expires_at_factory():
    return timezone.now() + timedelta(minutes=5)


class UserEmailVerification(models.Model):
    email = models.EmailField(
        help_text='이메일 주소',
        primary_key=True,
    )
    verification_code = models.TextField(
        help_text='인증 코드',
        null=False,
        blank=False,
    )
    verification_token = models.TextField(
        help_text='인증 토큰',
        null=True,
        blank=True,
    )
    expires_at = models.DateTimeField(default=default_expires_at_factory)
    created_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        EMAIL = 'email'
        VERIFICATION_CODE = 'verification_code'
        VERIFICATION_TOKEN = 'verification_token'
        EXPIRES_AT = 'expires_at'
        CREATED_AT = 'created_at'

    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()
