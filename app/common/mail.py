from django.core.mail import send_mail

from apps.background_task import background


@background
def schedule_mail(subject: str, message: str, recipient: str) -> None:
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[recipient],
        from_email=None,
        fail_silently=False,
    )
