import typing

from django.conf import settings

from tle.models import *
from tle.services.data.parser.parsers import *


DATA_DIR = settings.BASE_DIR / 'tle/services/data'


T = typing.TypeVar('T')


def get_model_parser(model_class: T) -> ModelParser[T]:
    PARSERS = {
        Problem: ProblemParser,
        ProblemTag: ProblemTagParser,
        SubmissionLanguage: SubmissionLanguageParser,
    }
    if model_class not in PARSERS:
        raise NotImplementedError(
            f'Parser for {model_class} is not implemented')
    return PARSERS[model_class]()


def get_model_default_json_file(model_class: T) -> str:
    FILES = {
        Problem: DATA_DIR / 'raw-problems.json',
        ProblemTag: DATA_DIR / 'raw-tags.json',
        SubmissionLanguage: DATA_DIR / 'raw-languages.json',
    }
    if model_class not in FILES:
        raise NotImplementedError(f'Default JSON file for {model_class} is not implemented')
    return FILES[model_class]


def parse(model_class: T, file: str = None) -> typing.List[T]:
    parser = get_model_parser(model_class)
    if file is None:
        file = get_model_default_json_file(model_class)
    return parser.parse_json(file, many=True)
