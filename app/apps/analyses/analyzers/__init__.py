from logging import getLogger

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.background_task.tasks import tasks
from apps.analyses.dto import ProblemAnalysisRawDTO
from apps.analyses.models import ProblemAnalysis
from apps.analyses.models import ProblemTag
from apps.analyses.analyzers.base import ProblemAnalyzer
from apps.analyses.analyzers.gemini import GeminiProblemAnalyzer
from apps.problems.dto import ProblemDTO
from apps.problems.models import Problem


logger = getLogger(__name__)


def get_analyzer() -> ProblemAnalyzer:
    return GeminiProblemAnalyzer.get_instance()


@receiver(post_save, sender=Problem)
def auto_analyze(sender, instance: Problem, created: bool, **kwargs):
    if created:
        schedule_analyze(instance.pk)


@tasks.background
def schedule_analyze(problem_id: int):
    logger.info(f'PK={problem_id} 문제의 분석 준비중.')
    problem: Problem = Problem.objects.get(pk=problem_id)
    problem_dto = problem.as_dto()
    logger.info('문제 분석기를 불러오는 중.')
    analyzer = get_analyzer()
    logger.info(f'{problem_dto} 문제의 분석 시작.')
    analysis_dto = analyzer.analyze(problem_dto)
    logger.info(f'{problem_dto} 문제의 분석 완료.')
    logger.info(f'{problem_dto} 문제의 분석 결과를 데이터베이스에 저장하는 중.')
    validate_analysis_dto_tags(analysis_dto)
    ProblemAnalysis.objects.create_from_dto(analysis_dto)
    logger.info(f'{problem_dto} 문제의 분석 결과를 데이터베이스에 저장 완료.')


def validate_analysis_dto_tags(analysis_dto: ProblemAnalysisRawDTO):
    for tag_key in analysis_dto.tags:
        try:
            ProblemTag.objects.get_by_key(tag_key)
        except ProblemTag.DoesNotExist:
            logger.warn(f'문제 분석 결과에 알 수 없는 태그 [{tag_key}] 가 포함된 것을 발견하였습니다.')
            ProblemTag.objects.create(**{
                ProblemTag.field_name.KEY: tag_key,
                ProblemTag.field_name.NAME_KO: f'존재하지 않는 태그: [{tag_key}]',
                ProblemTag.field_name.NAME_EN: f'존재하지 않는 태그: [{tag_key}]',
            })
