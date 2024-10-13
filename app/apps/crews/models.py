from __future__ import annotations

from textwrap import dedent
import typing

from django.contrib import admin
from django.core import validators
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone

from apps.boj.enums import BOJLevel
from apps.problems.models import ProblemDAO
from common.mail import schedule_mail
from users.models import User

from . import enums


class CrewManager(models.Manager['CrewDAO']):
    def as_member(self, user: User) -> models.QuerySet[CrewDAO]:
        return self.filter(**{CrewDAO.field_name.PK+'__in': self._ids_as_member(user)})

    def not_as_member(self, user: User) -> models.QuerySet[CrewDAO]:
        return self.exclude(**{CrewDAO.field_name.PK+'__in': self._ids_as_member(user)})

    def _ids_as_member(self, user: User) -> typing.List[int]:
        if user.is_anonymous:
            return []
        return CrewMemberDAO.objects \
            .filter(**{CrewMemberDAO.field_name.USER: user}) \
            .values_list(CrewMemberDAO.field_name.CREW, flat=True)


class CrewDAO(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text='크루 이름을 입력해주세요. (최대 20자)',
    )
    icon = models.TextField(
        choices=enums.EmojiChoices.choices,
        null=False,
        blank=False,
        default=enums.EmojiChoices.U1F6A2,  # :ship:
        help_text='크루 아이콘을 입력해주세요. (이모지)',
    )
    max_members = models.IntegerField(
        help_text='크루 최대 인원을 입력해주세요.',
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(8),
        ],
        default=8,
        blank=False,
        null=False,
    )
    notice = models.TextField(
        help_text='크루 공지를 입력해주세요.',
        null=True,
        blank=True,
        max_length=500,  # TODO: 최대 길이 제한이 적정한지 검토
    )
    custom_tags = models.JSONField(
        help_text='태그를 입력해주세요.',
        validators=[
            # TODO: 태그 형식 검사
        ],
        blank=True,
        default=list,
    )
    min_boj_level = models.IntegerField(
        help_text='최소 백준 레벨을 입력해주세요. 0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I',
        choices=BOJLevel.choices,
        default=BOJLevel.U,
    )
    is_recruiting = models.BooleanField(
        help_text='모집 중 여부를 입력해주세요.',
        default=True,
    )
    is_active = models.BooleanField(
        help_text='활동 중인지 여부를 입력해주세요.',
        default=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(auto_now=True)

    objects: CrewManager = CrewManager()

    class field_name:
        PK = 'pk'
        NAME = 'name'
        ICON = 'icon'
        MAX_MEMBERS = 'max_members'
        NOTICE = 'notice'
        CUSTOM_TAGS = 'custom_tags'
        MIN_BOJ_LEVEL = 'min_boj_level'
        IS_RECRUITING = 'is_recruiting'
        IS_ACTIVE = 'is_active'
        CREATED_AT = 'created_at'
        CREATED_BY = 'created_by'
        UPDATED_AT = 'updated_at'

    class method_name:
        GET_DISPLAY_NAME = 'get_display_name'
        GET_MEMBERS_COUNT = 'get_members_count'

    class Meta:
        verbose_name = 'Crew'
        verbose_name_plural = 'Crews'
        ordering = ['-updated_at']

    def __str__(self) -> str:
        return f'[{self.pk} : {self.icon} "{self.name}"]'

    def save(self, *args, **kwargs):
        with atomic():
            super().save(*args, **kwargs)
            self.add_member(self.created_by, is_captain=True)

    @admin.display(description='Display Name')
    def get_display_name(self) -> str:
        return f'{self.icon} {self.name}'

    def get_members(self) -> models.QuerySet[CrewMemberDAO]:
        return CrewMemberDAO.objects.filter(**{CrewMemberDAO.field_name.CREW: self})

    def get_captain(self) -> CrewMemberDAO:
        return CrewMemberDAO.objects.filter(**{
            CrewMemberDAO.field_name.CREW: self,
            CrewMemberDAO.field_name.IS_CAPTAIN: True,
        }).get()

    def get_submittable_languages(self) -> models.QuerySet[CrewSubmittableLanguageDAO]:
        return CrewSubmittableLanguageDAO.objects.filter(**{
            CrewSubmittableLanguageDAO.field_name.CREW: self,
        })

    def get_applications(self) -> models.QuerySet[CrewApplicationDAO]:
        return CrewApplicationDAO.objects.filter(**{CrewApplicationDAO.field_name.CREW: self})

    def is_captain(self, user: User) -> bool:
        return CrewMemberDAO.objects.filter(**{
            CrewMemberDAO.field_name.CREW: self,
            CrewMemberDAO.field_name.USER: user,
            CrewMemberDAO.field_name.IS_CAPTAIN: True,
        }).exists()

    def is_member(self, user: User) -> bool:
        return CrewMemberDAO.objects.filter(**{
            CrewMemberDAO.field_name.CREW: self,
            CrewMemberDAO.field_name.USER: user,
        }).exists()

    def is_appliable(self, user: User) -> bool:
        if user.is_anonymous:
            return False
        if not self.is_recruiting:
            return False
        if self.get_members().count() >= self.max_members:
            return False
        if self.is_member(user):
            return False
        if self.min_boj_level is None:
            return True
        return self.min_boj_level <= user.get_boj_level()

    def apply(self, applicant: User, message: str, force=False) -> CrewApplicationDAO:
        if self.is_appliable(applicant) or force:
            application = CrewApplicationDAO.objects.create(**{
                CrewApplicationDAO.field_name.CREW: self,
                CrewApplicationDAO.field_name.APPLICANT: applicant,
                CrewApplicationDAO.field_name.MESSAGE: message,
            })
            application.send_on_create_notification()
            return application

    def add_member(self, user: User, is_captain=False) -> CrewMemberDAO:
        with atomic():
            CrewMemberDAO.objects \
                .filter(**{CrewMemberDAO.field_name.CREW: self, CrewMemberDAO.field_name.IS_CAPTAIN: True}) \
                .update(**{CrewMemberDAO.field_name.IS_CAPTAIN: False})
            return CrewMemberDAO.objects.create(**{
                CrewMemberDAO.field_name.CREW: self,
                CrewMemberDAO.field_name.USER: user,
                CrewMemberDAO.field_name.IS_CAPTAIN: is_captain,
            })

    def add_activity(self, name: str, start_at: timezone.datetime, end_at: timezone.datetime) -> CrewActivityDAO:
        return CrewActivityDAO.objects.create(**{
            CrewActivityDAO.field_name.CREW: self,
            CrewActivityDAO.field_name.NAME: name,
            CrewActivityDAO.field_name.START_AT: start_at,
            CrewActivityDAO.field_name.END_AT: end_at,
        })

    def set_submittable_languages(self, languages: typing.Tuple[str]) -> None:
        instances = []
        for language in languages:
            instance = CrewSubmittableLanguageDAO(**{
                CrewSubmittableLanguageDAO.field_name.CREW: self,
                CrewSubmittableLanguageDAO.field_name.LANGUAGE: language,
            })
            instances.append(instance)
        with atomic():
            self.get_submittable_languages().delete()
            CrewSubmittableLanguageDAO.objects.bulk_create(instances)


class CrewMemberDAO(models.Model):
    crew = models.ForeignKey(
        CrewDAO,
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
        PK = 'pk'
        CREW = 'crew'
        USER = 'user'
        IS_CAPTAIN = 'is_captain'
        CREATED_AT = 'created_at'

    class Meta:
        verbose_name = 'Crew Member'
        verbose_name_plural = 'Crew Members'
        constraints = [
            models.UniqueConstraint(
                fields=['crew', 'user'],
                name='unique_member_per_crew'
            ),
        ]
        ordering = ['created_at']

    def __str__(self) -> str:
        return f'[{self.pk} : "{self.user.username}"@"{self.crew}"]'


class CrewSubmittableLanguageDAO(models.Model):
    crew = models.ForeignKey(
        CrewDAO,
        on_delete=models.CASCADE,
    )
    language = models.TextField(
        choices=enums.ProgrammingLanguageChoices.choices,
        help_text='언어 키를 입력해주세요. (최대 20자)',
    )

    class field_name:
        PK = 'pk'
        CREW = 'crew'
        LANGUAGE = 'language'

    class Meta:
        verbose_name = 'Crew Submittable Language'
        verbose_name_plural = 'Crew Submittable Languages'
        ordering = ['crew']

    def __str__(self) -> str:
        return f'[{self.pk} : #{self.language}]'


class CrewApplicationDAO(models.Model):
    crew = models.ForeignKey[CrewDAO](
        CrewDAO,
        on_delete=models.CASCADE,
        help_text='크루를 입력해주세요.',
    )
    applicant = models.ForeignKey[User](
        User,
        on_delete=models.CASCADE,
        help_text='지원자를 입력해주세요.',
    )
    message = models.TextField(
        help_text='가입 메시지를 입력해주세요.',
        null=True,
        blank=True,
    )
    is_pending = models.BooleanField(
        default=True,
        help_text="아직 수락/거절 되지 않았다면 True.",
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
        APPLICANT = 'applicant'
        MESSAGE = 'message'
        IS_PENDING = 'is_pending'
        IS_ACCEPTED = 'is_accepted'
        CREATED_AT = 'created_at'
        REVIEWED_AT = 'reviewed_at'
        REVIEWED_BY = 'reviewed_by'

    class Meta:
        verbose_name = 'Crew Application'
        verbose_name_plural = 'Crew Applications'
        ordering = ['reviewed_by', 'created_at']

    def __repr__(self) -> str:
        return f'{self.crew.__repr__()} ← {self.applicant.__repr__()} : "{self.message}"'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'

    def accept(self, reviewed_by: User):
        self.is_pending = False
        self.is_accepted = True
        self.reviewed_by = reviewed_by
        self.reviewed_at = timezone.now()
        with atomic():
            self.save()
            self.crew.add_member(self.applicant)
        self.send_on_accept_notification()

    def reject(self, reviewed_by: User):
        self.is_pending = False
        self.is_accepted = False
        self.reviewed_by = reviewed_by
        self.reviewed_at = timezone.now()
        self.save()
        self.send_on_reject_notification()

    def send_on_create_notification(self):
        schedule_mail(
            subject='[Time Limit Exceeded] 새로운 크루 가입 신청이 도착했습니다',
            message=dedent(f"""
                [{self.crew.get_display_name()}]에 새로운 가입 신청이 왔어요!

                지원자: {self.applicant.username}
                지원자의 백준 아이디(레벨): {self.applicant.boj_username} ({self.applicant.get_boj_level().get_name()})

                지원자의 메시지:
                ```
                {self.message}
                ```

                수락하시려면 [여기]를 클릭해주세요.
            """),
            recipient=self.crew.created_by.email,
        )

    def send_on_accept_notification(self):
        schedule_mail(
            subject='[Time Limit Exceeded] 새로운 크루 가입 신청이 승인되었습니다',
            message=dedent(f"""
                [{self.crew.get_display_name()}]에 가입하신 것을 축하해요!

                [여기]를 눌러 크루 대시보드로 바로가기
            """),
            recipient=self.applicant.email,
        )

    def send_on_reject_notification(self):
        schedule_mail(
            subject='[Time Limit Exceeded] 새로운 크루 가입 신청이 거절되었습니다',
            message=dedent(f"""
                [{self.crew.get_display_name()}]에 아쉽게도 가입하지 못했어요.
            """),
            recipient=self.applicant.email,
        )


class CrewActivityDAO(models.Model):
    crew = models.ForeignKey(
        CrewDAO,
        on_delete=models.CASCADE,
        help_text='크루를 입력해주세요.',
    )
    name = models.TextField(
        help_text='활동 이름을 입력해주세요. (예: "1회차")',
        default='이름 없음',
    )
    start_at = models.DateTimeField(
        help_text='활동 시작 일자를 입력해주세요.',
    )
    end_at = models.DateTimeField(
        help_text='활동 종료 일자를 입력해주세요.',
    )

    class field_name:
        CREW = 'crew'
        NAME = 'name'
        START_AT = 'start_at'
        END_AT = 'end_at'

    class method_name:
        IS_IN_PROGRESS = 'is_in_progress'
        HAS_STARTED = 'has_started'
        HAS_ENDED = 'has_ended'

    class Meta:
        verbose_name = 'Crew Activity'
        verbose_name_plural = 'Crew Activities'
        ordering = ['start_at']
        get_latest_by = ['end_at']

    def __str__(self) -> str:
        return f'[{self.pk}: "{self.name}"@"{self.crew.name}" ({self.start_at.date()} ~ {self.end_at.date()})]'

    @admin.display(boolean=True, description='진행 중')
    def is_in_progress(self) -> bool:
        return self.has_started() and not self.has_ended()

    @admin.display(boolean=True, description='시작 됨')
    def has_started(self) -> bool:
        return self.start_at <= timezone.now()

    @admin.display(boolean=True, description='종료 됨')
    def has_ended(self) -> bool:
        return self.end_at < timezone.now()

    def update_name(self) -> str:
        count = CrewActivityDAO.objects \
            .filter(**{CrewActivityDAO.field_name.CREW: self.crew}) \
            .count()
        self.name = f'{count+1}회차'

    def get_problems(self) -> models.QuerySet[CrewProblemDAO]:
        return CrewProblemDAO.objects.filter(**{CrewProblemDAO.field_name.ACTIVITY: self})

    def add_problem(self, problem_ref: ProblemDAO, order: int) -> CrewProblemDAO:
        return CrewProblemDAO.objects.create(**{
            CrewProblemDAO.field_name.CREW: self.crew,
            CrewProblemDAO.field_name.ACTIVITY: self,
            CrewProblemDAO.field_name.PROBLEM: problem_ref,
            CrewProblemDAO.field_name.ORDER: order,
        })

    def set_problem_refs(self, problem_refs: typing.Tuple[ProblemDAO]) -> None:
        problem_order_map = dict()
        for order, problem_ref in enumerate(problem_refs, start=1):
            problem_order_map[problem_ref] = order
        with atomic():
            # 기존 문제들 중 새로운 문제들에 포함되지 않는 것들을 제거
            self.get_problems() \
                .exclude(**{CrewProblemDAO.field_name.PROBLEM+'__in': problem_refs}) \
                .delete()
            # 기존 문제들의 순서를 업데이트
            for problem in self.get_problems():
                problem.order = problem_order_map.pop(problem.problem)
                problem.save()
            # 새로운 문제들을 추가
            for problem_ref, order in problem_order_map.items():
                self.add_problem(problem_ref, order)


class CrewProblemDAO(models.Model):
    crew = models.ForeignKey(
        CrewDAO,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    activity = models.ForeignKey(
        CrewActivityDAO,
        on_delete=models.CASCADE,
        help_text='활동을 입력해주세요.',
    )
    problem = models.ForeignKey(
        ProblemDAO,
        on_delete=models.PROTECT,
        help_text='문제를 입력해주세요.',
    )
    order = models.IntegerField(
        help_text='문제 순서를 입력해주세요.',
        validators=[
            validators.MinValueValidator(1),
        ],
    )

    class field_name:
        PK = 'pk'
        CREW = 'crew'
        ACTIVITY = 'activity'
        PROBLEM = 'problem'
        ORDER = 'order'

    class Meta:
        verbose_name = 'Crew Problem'
        verbose_name_plural = 'Crew Problems'
        ordering = ['order']
        unique_together = ['activity', 'problem']

    def save(self, *args, **kwargs) -> None:
        assert self.crew == self.activity.crew
        return super().save(*args, **kwargs)

    def __repr__(self) -> str:
        return f'{self.activity.__repr__()} ← #{self.order} {self.problem.__repr__()}'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
