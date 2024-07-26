from django.db import models, transaction
from django.utils import timezone

from users.models import User
from tle.models.dao.crew import Crew
from tle.models.dao.crew_member import CrewMember


class CrewApplicant(models.Model):
    crew = models.ForeignKey[Crew](
        Crew,
        on_delete=models.CASCADE,
        help_text='크루를 입력해주세요.',
    )
    user = models.ForeignKey[User](
        User,
        on_delete=models.CASCADE,
        help_text='유저를 입력해주세요.',
    )
    message = models.TextField(
        help_text='가입 메시지를 입력해주세요.',
        null=True,
        blank=True,
    )
    is_accepted = models.BooleanField(
        default=False,
        help_text='수락 여부를 입력해주세요.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(
        help_text='리뷰한 시간을 입력해주세요.',
        null=True,
        blank=True,
        default=None,
    )
    reviewed_by = models.ForeignKey[User](
        User,
        related_name='reviewed_applicants',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    class field_name:
        CREW = 'crew'
        USER = 'user'
        MESSAGE = 'message'
        IS_ACCEPTED = 'is_accepted'
        CREATED_AT = 'created_at'
        REVIEWED_AT = 'reviewed_at'
        REVIEWED_BY = 'reviewed_by'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['crew', 'user'],
                name='unique_applicant_per_crew',
            ),
        ]
        ordering = ['reviewed_by', 'created_at']

    def __repr__(self) -> str:
        return f'{self.crew.__repr__()} ← {self.user.__repr__()} : "{self.message}"'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'

    def save(self, *args, **kwargs) -> None:
        # 같은 크루에 여러 번 가입하는 것을 방지
        if self.crew.members.filter(user=self.user).exists():
            raise ValueError('이미 가입한 크루에 가입 신청을 할 수 없습니다.')

        return super().save(*args, **kwargs)

    def accept(self, commit=True) -> CrewMember:
        """크루 가입 신청을 수락합니다."""
        member = CrewMember(
            crew=self.crew,
            user=self.user,
        )
        self.is_accepted = True
        self.reviewed_at = timezone.now()
        if commit:
            with transaction.atomic():
                member.save()
                self.save()
        return member

    def reject(self, commit=True):
        """크루 가입 신청을 거절합니다."""
        self.is_accepted = False
        self.reviewed_at = timezone.now()
        if commit:
            self.save()
