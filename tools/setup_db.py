"""
Use this like:

$ python manage.py shell < tools/db_setup.py
"""

import dataclasses
import json
from typing import List


@dataclasses.dataclass
class DisplayNameJSON:
    language: str
    name: str
    short: str


@dataclasses.dataclass
class AliasJSON:
    alias: str


@dataclasses.dataclass
class TagJSON:
    key: str
    isMeta: bool
    bojTagId: int
    problemCount: int
    displayNames: List[DisplayNameJSON]
    aliases: List[AliasJSON]


@dataclasses.dataclass
class LanguageJSON:
    key: str
    bojId: int
    displayName: str
    extension: str


def load_tags(file='../tools/tags.json') -> List[TagJSON]:
    with open(file) as f:
        raw_tags = json.load(f)
    tags = []
    for item in raw_tags['items']:
        tag = TagJSON(**item)
        tag.displayNames = [DisplayNameJSON(**display_name) for display_name in item["displayNames"]]
        tag.aliases = [AliasJSON(**alias) for alias in item["aliases"]]
        tags.append(tag)
    return tags


def load_languages(file='../tools/languages.json') -> List[str]:
    with open(file) as f:
        raw_languages = json.load(f)
    languages = []
    for item in raw_languages['items']:
        languages.append(LanguageJSON(**item))
    return languages


from django.db.transaction import atomic

from boj.models import BOJTag
from core.models import Language
from core.models import Tag


with atomic():
    for tag_data in load_tags():
        tag = Tag.objects.get_or_create(key=tag_data.key)[0]
        tag.name_ko = next(filter(lambda x: x.language == 'ko', tag_data.displayNames)).name
        tag.name_en = next(filter(lambda x: x.language == 'en', tag_data.displayNames)).name
        tag.full_clean()
        tag.save()
        boj_tag = BOJTag.objects.get_or_create(
            boj_id=tag_data.bojTagId,
            tag=tag,
        )[0]
        boj_tag.full_clean()
        boj_tag.save()


with atomic():
    for lang_data in load_languages():
        lang = Language.objects.get_or_create(
            pk=lang_data.bojId,
            key=lang_data.key
        )[0]
        lang.name = lang_data.displayName
        lang.extension = lang_data.extension
        lang.full_clean()
        lang.save()
