from django.db.models.signals import post_save
from django.dispatch import receiver

from crews.models import (
    Crew,
    CrewMember,
    CrewSubmittableLanguage,
    ProgrammingLanguageChoices,
)
from users.models import User


@receiver(post_save, sender=Crew)
def auto_create_captain(sender, instance: Crew, created: bool, **kwargs):
    """크루 생성 시 선장을 자동으로 생성합니다."""
    if created:
        CrewMember.objects.create(**{
            CrewMember.field_name.CREW: instance,
            CrewMember.field_name.USER: instance.created_by,
            CrewMember.field_name.IS_CAPTAIN: True,
        })


def set_crew_submittable_languages(crew: Crew, languages: list):
    """크루의 제출 가능 언어를 설정합니다."""
    for language in languages:
        for choice in ProgrammingLanguageChoices.choices:
            if language == choice[0]:
                raise ValueError('Invalid language')
    CrewSubmittableLanguage.objects.filter(**{
        CrewSubmittableLanguage.field_name.CREW: crew,
    }).delete()
    CrewSubmittableLanguage.objects.bulk_create([
        CrewSubmittableLanguage(**{
            CrewSubmittableLanguage.field_name.CREW: crew,
            CrewSubmittableLanguage.field_name.LANGUAGE: language,
        }) for language in languages
    ])


def get_members(crew: Crew):
    return CrewMember.objects.filter(**{
        CrewMember.field_name.CREW: crew,
    })


def is_member(crew: Crew, user: User) -> bool:
    return CrewMember.objects.filter(**{
        CrewMember.field_name.CREW: crew,
        CrewMember.field_name.USER: user,
    }).exists()


def is_joinable(crew: Crew, user: User) -> bool:
    if not crew.is_recruiting:
        return False
    if get_members(crew).count() >= crew.max_members:
        return False
    if is_member(crew, user):
        return False
    if crew.min_boj_level is not None:
        return bool(
            (user.boj_level is not None) and
            (user.boj_level >= crew.min_boj_level)
        )
    return True
