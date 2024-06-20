from django.core.validators import MinValueValidator
from django.db import models

from boj.models import *
from core.models import *
from problem.models import *
from user.models import *


class Crew(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '크루 이름을 입력해주세요. (최대 20자)'
        ),
    )
    emoji = models.CharField(
        max_length=2,
        help_text=(
            '크루 아이콘을 입력해주세요. (이모지)'
        ),
        validators=[
            # TODO: 이모지 형식 검사
        ],
        null=True,
        blank=True,
    )
    captain = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='crews_as_captain',
        help_text=(
            '크루장을 입력해주세요.'
        ),
    )
    notice = models.TextField(
        help_text=(
            '크루 공지를 입력해주세요.'
        ),
        null=True,
        blank=True,
    )
    languages = models.ManyToManyField(
        Language,
        related_name='crews',
        help_text=(
            '유저가 사용 가능한 언어를 입력해주세요.'
        ),
    )
    max_member = models.IntegerField(
        help_text=(
            '크루 최대 인원을 입력해주세요.'
        ),
        validators=[
            MinValueValidator(1),
            # TODO: 최대 인원 제한
        ],
    )
    is_boj_user_only = models.BooleanField(
        help_text=(
            '백준 아이디 필요 여부를 입력해주세요.'
        ),
        default=False,
    )
    min_boj_tier = models.IntegerField(
        help_text=(
            '최소 백준 레벨을 입력해주세요. ',
            '0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I'
        ),
        choices=BOJLevel.choices,
        blank=True,
        null=True,
        default=None,
    )
    max_boj_tier = models.IntegerField(
        help_text=(
            '최대 백준 레벨을 입력해주세요. ',
            '0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I'
        ),
        validators=[
            # TODO: 최대 레벨이 최소 레벨보다 높은지 검사
        ],
        choices=BOJLevel.choices,
        blank=True,
        null=True,
        default=None,
    )
    tags = models.JSONField(
        help_text=(
            '태그를 입력해주세요.'
        ),
        validators=[
            # TODO: 태그 형식 검사
        ],
        blank=True,
        default=list,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f'[{self.emoji} {self.name}]'

    def __str__(self) -> str:
        member_count = f'({self.members.count()}/{self.max_member})'
        return f'{self.pk} : {self.__repr__()} {member_count} ← {self.captain.__repr__()}'


class CrewMember(models.Model):
    # TODO: 같은 크루에 여러 번 가입하는 것을 막기 위한 로직 추가
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name='members',
        help_text=(
            '크루를 입력해주세요.'
        ),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='crews',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f'[{self.crew.emoji} {self.crew.name}] ← [@{self.user.username}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


class CrewMemberRequest(models.Model):
    # TODO: 같은 크루에 여러 번 가입하는 것을 막기 위한 로직 추가
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name='requests',
        help_text=(
            '크루를 입력해주세요.'
        ),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='crew_requests',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    message = models.TextField(
        help_text=(
            '가입 메시지를 입력해주세요.'
        ),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f'{self.crew.__repr__()} ← {self.user.__repr__()} : "{self.message}"'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


class CrewActivity(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name='activities',
        help_text=(
            '크루를 입력해주세요.'
        ),
    )
    start_at = models.DateTimeField(
        help_text=(
            '활동 시작 일자를 입력해주세요.'
        ),
    )
    end_at = models.DateTimeField(
        help_text=(
            '활동 종료 일자를 입력해주세요.'
        ),
    )

    def __repr__(self) -> str:
        return f'{self.crew.__repr__()} ← [{self.start_at.date()} ~ {self.end_at.date()}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


class CrewActivityProblem(models.Model):
    activity = models.ForeignKey(
        CrewActivity,
        on_delete=models.CASCADE,
        related_name='problems',
        help_text=(
            '활동을 입력해주세요.'
        ),
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.PROTECT,
        related_name='activities',
        help_text=(
            '문제를 입력해주세요.'
        ),
    )
    order = models.IntegerField(
        help_text=(
            '문제 순서를 입력해주세요.'
        ),
        validators=[
            MinValueValidator(1),
            # TODO: 다른 문제 순서와 겹치지 않도록 검사
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f'{self.activity.__repr__()} ← #{self.order} {self.problem.__repr__()}'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


class CrewActivityProblemSubmission(models.Model):
    # TODO: 같은 문제에 여러 번 제출 하는 것을 막기 위한 로직 추가
    activity_problem = models.ForeignKey(
        CrewActivityProblem,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text=(
            '활동 문제를 입력해주세요.'
        ),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    code = models.TextField(
        help_text=(
            '유저의 코드를 입력해주세요.'
        ),
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        related_name='submissions',
        help_text=(
            '유저의 코드 언어를 입력해주세요.'
        ),
    )
    is_correct = models.BooleanField(
        help_text=(
            '유저의 코드가 정답인지 여부를 입력해주세요.'
        ),
    )
    is_help_needed = models.BooleanField(
        help_text=(
            '유저의 코드에 도움이 필요한지 여부를 입력해주세요.'
        ),
        default=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f'{self.activity_problem.__repr__()} ← {self.user.__repr__()} ({self.language.name})'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


class CrewActivityProblemSubmissionComment(models.Model):
    submission = models.ForeignKey(
        CrewActivityProblemSubmission,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text=(
            '제출을 입력해주세요.'
        ),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    content = models.TextField(
        help_text=(
            '댓글을 입력해주세요.'
        ),
    )
    line_number_start = models.IntegerField(
        help_text=(
            '댓글 시작 라인을 입력해주세요.'
        ),
        validators=[
            MinValueValidator(1),
        ],
    )
    line_number_end = models.IntegerField(
        help_text=(
            '댓글 종료 라인을 입력해주세요.'
        ),
        validators=[
            MinValueValidator(1),
            # TODO: 시작 라인보다 작지 않도록 검사
            # TODO: 코드 라인 수보다 크지 않도록 검사
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        line_range = f'L{self.line_number_start}:L{self.line_number_end}'
        return f'{self.submission.__repr__()} ← {self.user.__repr__()} {line_range} "{self.content}"'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
