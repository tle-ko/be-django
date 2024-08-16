from django.db import models

from users.models import User
from crews.models.crew import Crew
from crews.models.crew_member import CrewMember


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
        ordering = ['reviewed_by', 'created_at']

    def __repr__(self) -> str:
        return f'{self.crew.__repr__()} ← {self.user.__repr__()} : "{self.message}"'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'

    def save(self, *args, **kwargs) -> None:
        try:
            # 같은 크루에 여러 번 가입하는 것을 방지
            assert not CrewMember.objects.filter(**{
                CrewMember.field_name.CREW: self.crew,
                CrewMember.field_name.USER: self.user,
            }).exclude(pk=self.pk).exists(), '이미 가입한 크루에 가입 신청을 할 수 없습니다.'
            # 아직 검토되지 않은 신청이 있으면 가입 불가
            assert not CrewApplicant.objects.filter(**{
                CrewApplicant.field_name.CREW: self.crew,
                CrewApplicant.field_name.USER: self.user,
                CrewApplicant.field_name.REVIEWED_BY: None,
            }).exclude(pk=self.pk).exists(), '크루에 아직 검토되지 않은 지원 이력이 있습니다.'
        except AssertionError as e:
            raise ValueError from e
        else:
            return super().save(*args, **kwargs)
