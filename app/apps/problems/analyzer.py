import typing

from django.db.models.signals import post_save
from django.db.transaction import atomic
from django.dispatch import receiver

from apps.background_task.tasks import tasks
from apps.boj.proxy import BOJTag
from apps.llms.proxy import TextGeneration

from . import enums
from . import models
from . import prompts


def text_generate(prompt: str) -> int:
    obj = TextGeneration(**{
        TextGeneration.field_name.REQUEST: prompt,
    })
    obj.generate()
    return obj.pk


def load_generated_text(text_generation_id: int) -> str:
    return TextGeneration.objects.get(pk=text_generation_id).response


@tasks.background
def schedule_analysis(problem_ref_id: int,
                      tags_text_generation_id: typing.Optional[int] = None,
                      time_complexity_text_generation_id: typing.Optional[int] = None,
                      difficulty_text_generation_id: typing.Optional[int] = None,
                      hints_text_generation_id: typing.Optional[int] = None):

    problem = models.ProblemDAO.objects.get(pk=problem_ref_id)

    if tags_text_generation_id is None:
        prompt = prompts.TagPromptHandler().create_propmt(problem)
        tags_text_generation_id = text_generate(prompt)
        schedule_analysis(problem_ref_id,
                          tags_text_generation_id)
        return

    if time_complexity_text_generation_id is None:
        prompt = prompts.TimeComplexityPromptHandler().create_propmt(problem)
        time_complexity_text_generation_id = text_generate(prompt)
        schedule_analysis(problem_ref_id,
                          tags_text_generation_id,
                          time_complexity_text_generation_id)
        return

    if difficulty_text_generation_id is None:
        prompt = prompts.DifficultyPromptHandler().create_propmt(problem)
        difficulty_text_generation_id = text_generate(prompt)
        schedule_analysis(problem_ref_id,
                          tags_text_generation_id,
                          time_complexity_text_generation_id,
                          difficulty_text_generation_id)
        return

    if hints_text_generation_id is None:
        context = {
            'tags': prompts.TagPromptHandler().parse_response(load_generated_text(tags_text_generation_id)),
            'time_complexity': prompts.TimeComplexityPromptHandler().parse_response(load_generated_text(time_complexity_text_generation_id)),
            'difficulty': prompts.DifficultyPromptHandler().parse_response(load_generated_text(difficulty_text_generation_id)),
        }
        prompt = prompts.HintsPromptHandler().create_propmt(problem, context)
        hints_text_generation_id = text_generate(prompt)
        schedule_analysis(problem_ref_id,
                          tags_text_generation_id,
                          time_complexity_text_generation_id,
                          difficulty_text_generation_id,
                          hints_text_generation_id)
        return

    # All text generation is done
    context = {
        'tags': prompts.TagPromptHandler().parse_response(load_generated_text(tags_text_generation_id)),
        'time_complexity': prompts.TimeComplexityPromptHandler().parse_response(load_generated_text(time_complexity_text_generation_id)),
        'difficulty': prompts.DifficultyPromptHandler().parse_response(load_generated_text(difficulty_text_generation_id)),
        'hints': prompts.HintsPromptHandler().parse_response(load_generated_text(hints_text_generation_id)),
    }
    with atomic():
        analysis = models.ProblemAnalysisDAO.objects.create(**{
            models.ProblemAnalysisDAO.field_name.PROBLEM: problem,
            models.ProblemAnalysisDAO.field_name.DIFFICULTY: enums.ProblemDifficulty.from_label(context['difficulty']),
            models.ProblemAnalysisDAO.field_name.TIME_COMPLEXITY: context['time_complexity'],
            models.ProblemAnalysisDAO.field_name.HINTS: context['hints'],
        })
        for tag_key in context['tags']:
            tag = BOJTag.objects.get_by_key(tag_key)
            models.ProblemAnalysisTagDAO.objects.create(**{
                models.ProblemAnalysisTagDAO.field_name.ANALYSIS: analysis,
                models.ProblemAnalysisTagDAO.field_name.TAG: tag,
            })
