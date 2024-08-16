from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from crews.models.crew import Crew


class CrewMember(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        help_text='크루를 입력해주세요.',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='유저를 입력해주세요.',
    )
    is_captain = models.BooleanField(
        default=False,
        help_text='크루장 여부',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        CREW = 'crew'
        USER = 'user'
        IS_CAPTAIN = 'is_captain'
        CREATED_AT = 'created_at'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['crew', 'user'],
                name='unique_member_per_crew'
            ),
        ]
        ordering = ['created_at']


@receiver(post_save, sender=Crew)
def auto_create_captain(sender, instance: Crew, created: bool, **kwargs):
    """크루 생성 시 선장을 자동으로 생성합니다."""
    if created:
        CrewMember.objects.create(**{
            CrewMember.field_name.CREW: instance,
            CrewMember.field_name.USER: instance.created_by,
            CrewMember.field_name.IS_CAPTAIN: True,
        })
