"""
Use this like:

$ python manage.py shell < tools/db_setup.py
"""

import dataclasses
import json
from typing import List


@dataclasses.dataclass
class DisplayName:
    language: str
    name: str
    short: str


@dataclasses.dataclass
class Alias:
    alias: str


@dataclasses.dataclass
class Tag:
    key: str
    isMeta: bool
    bojTagId: int
    problemCount: int
    displayNames: List[DisplayName]
    aliases: List[Alias]



def load_tags(file='tools/tags.json') -> List[Tag]:
    with open(file) as f:
        raw_tags = json.load(f)
    tags = []
    for item in raw_tags['items']:
        tag = Tag(**item)
        tag.displayNames = [DisplayName(**display_name) for display_name in item["displayNames"]]
        tag.aliases = [Alias(**alias) for alias in item["aliases"]]
        tags.append(tag)
    return tags


from django.db.transaction import atomic

from boj.models import BOJTag
from core.models import DSA


with atomic():
    for tag in load_tags():
        dsa = DSA.objects.get_or_create(key=tag.key)[0]
        dsa.name_ko = next(filter(lambda x: x.language == 'ko', tag.displayNames)).name
        dsa.name_en = next(filter(lambda x: x.language == 'en', tag.displayNames)).name
        dsa.save()

        boj_tag = BOJTag.objects.get_or_create(boj_id=tag.bojTagId)[0]
        boj_tag.tag = dsa
        boj_tag.save()
