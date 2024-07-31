"""이 서비스는 사용자 확인 절차를 수행하는 데 필요한 기능을 제공합니다.

사용자 확인 절차는 다음과 같습니다:
1. 사용자가 이메일 주소를 입력합니다.
2. 서버는 해당 이메일 주소로 인증 코드를 전송합니다.
3. 사용자는 인증 코드를 입력합니다.
4. 서버는 인증 코드를 확인합니다.
5. 서버는 인증 코드를 확인한 사용자에게 인증 토큰을 전송합니다.
6. 사용자는 회원가입 절차에서 인증 토큰을 입력합니다.
7. 서버는 인증 토큰을 확인하여 사용자를 확인합니다.
"""
from hashlib import sha256
from random import randint

from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from users.models import User, UserEmailVerification


class VerificationService:
    @staticmethod
    def is_verified(email: str) -> bool:
        return User.objects.filter(**{
            User.field_name.EMAIL: email,
        }).exists()

    @staticmethod
    def get_verification_code(email: str) -> str:
        if has_verification_code(email):
            if not (obj := get_verification_object(email)).is_expired():
                return obj.verification_code
            else:
                obj.delete()
        verification_code = generate_verification_code()
        create_verification_object(email, verification_code)
        return verification_code

    @staticmethod
    def send_verification_code(email: str, verification_code: str) -> str:
        send_mail(
            subject='[Time Limit Exceeded] 이메일 주소 인증 코드',
            message=f'인증 코드: {verification_code}',
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

    @staticmethod
    def get_verification_token(email: str, verification_code: str) -> str:
        VerificationService.validate_verification_code(
            email, verification_code)
        verification_token = generate_verification_token()
        obj = get_verification_object(email)
        obj.verification_token = verification_token
        obj.save()
        return verification_token

    @staticmethod
    def validate_verification_code(email: str, verification_code: str) -> None:
        if not has_verification_code(email):
            raise ValidationError('Verification code does not exist.')
        obj = get_verification_object(email)
        if obj.is_expired():
            raise ValidationError('Verification code is expired.')
        if obj.verification_code != verification_code:
            raise ValidationError('Verification code is invalid.')

    @staticmethod
    def validate_verification_token(email: str, verification_token: str) -> None:
        if not has_verification_code(email):
            raise ValidationError('Verification token does not exist.')
        obj = get_verification_object(email)
        if obj.verification_token != verification_token:
            raise ValidationError('Verification token is invalid.')


def has_verification_code(email: str) -> bool:
    return UserEmailVerification.objects.filter(**{
        UserEmailVerification.field_name.EMAIL: email
    }).exists()


def create_verification_object(email: str, verification_code: str) -> UserEmailVerification:
    return UserEmailVerification.objects.create(**{
        UserEmailVerification.field_name.EMAIL: email,
        UserEmailVerification.field_name.VERIFICATION_CODE: verification_code
    })


def get_verification_object(email: str) -> UserEmailVerification:
    return UserEmailVerification.objects.get(**{
        UserEmailVerification.field_name.EMAIL: email
    })


def generate_verification_code(length: int = 6) -> str:
    return ''.join(chr(randint(ord('A'), ord('Z'))) for _ in range(length))


def generate_verification_token() -> str:
    seed = generate_verification_code()  # TODO: Use better seed
    return sha256(seed.encode()).hexdigest()
