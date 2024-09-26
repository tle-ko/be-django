from textwrap import dedent

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.background_task.tasks import tasks
from users.models import UserEmailVerification


@receiver(post_save, sender=UserEmailVerification)
def notify_on_code_generated(sender, instance: UserEmailVerification, created: bool, **kwargs):
    if not instance.is_expired():
        subject = '[Time Limit Exceeded] 이메일 주소 인증 코드'
        message = dedent(f"""
            인증 코드: {instance.verification_code}
        """)
        recipient = instance.email
        _schedule_mail(subject, message, recipient)


@tasks.background
def _schedule_mail(subject: str, message: str, recipient: str) -> None:
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[recipient],
        from_email=None,
        fail_silently=False,
    )
