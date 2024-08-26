from logging import getLogger
from typing import List
from typing import Optional

from background_task import background
from django.db.models import QuerySet
from django.db.transaction import atomic

from problems import dto
from problems import enums
from problems import models
from problems.services.base import ProblemService
from problems.services.analyzers import ProblemAnalyzer
from problems.services.analyzers import GeminiProblemAnalyzer


logger = getLogger('problems.services')


class ConcreteProblemService(ProblemService):
    def __init__(self, instance: models.Problem) -> None:
        super().__init__(instance)
        self._analysis = None

    def query_analyses(self) -> QuerySet[models.ProblemAnalysis]:
        return models.ProblemAnalysis.objects.filter(**{
            models.ProblemAnalysis.field_name.PROBLEM: self.instance,
        })

    def query_analysis_tags(self) -> QuerySet[models.ProblemAnalysisTag]:
        if not self.is_analyzed():
            return models.ProblemAnalysisTag.objects.none()
        else:
            return models.ProblemAnalysisTag.objects.filter(**{
                models.ProblemAnalysisTag.field_name.ANALYSIS: self.get_analysis(),
            })

    def query_tags(self) -> QuerySet[models.ProblemTag]:
        return models.ProblemTag.objects.filter(**{
            models.ProblemTag.field_name.KEY+'__in': self.tags(),
        })

    def get_analysis(self) -> Optional[models.ProblemAnalysis]:
        try:
            self._analysis = self.query_analyses().latest()
        except models.ProblemAnalysis.DoesNotExist:
            self._analysis = None
        finally:
            return self._analysis

    def is_analyzed(self) -> bool:
        return self.get_analysis() is not None

    def analyze(self) -> None:
        schedule_analyze(self.instance.pk)

    def difficulty(self) -> enums.ProblemDifficulty:
        if (analysis := self.get_analysis()) is None:
            return enums.ProblemDifficulty.UNDER_ANALYSIS
        return enums.ProblemDifficulty(analysis.difficulty)

    def time_complexity(self) -> str:
        if (analysis := self.get_analysis()) is None:
            return '?'
        return analysis.time_complexity

    def tags(self) -> List[str]:
        return self.query_analysis_tags().select_related(
            models.ProblemAnalysisTag.field_name.TAG,
        ).values_list(models.ProblemAnalysisTag.field_name.TAG+'__'+models.ProblemTag.field_name.KEY)

    def hints(self) -> List[str]:
        if (analysis := self.get_analysis()) is None:
            return []
        return analysis.hint


@background
def schedule_analyze(problem_id: int):
    logger.info(f'PK={problem_id} 문제의 분석 준비중.')
    problem = get_problem(problem_id)
    problem_dto = get_problem_dto(problem)
    problem_repr = f'PK={problem_id} ({problem_dto.title})'
    logger.info('문제 분석기를 불러오는 중.')
    analyzer = get_analyzer()
    logger.info(f'{problem_repr} 문제의 분석 시작.')
    analysis_dto = analyzer.analyze(problem_dto)
    logger.info(f'{problem_repr} 문제의 분석 완료.')
    logger.info(f'{problem_repr} 문제의 분석 결과를 데이터베이스에 저장하는 중.')
    save_analysis(problem, analysis_dto)
    logger.info(f'{problem_repr} 문제의 분석 결과를 데이터베이스에 저장 완료.')


def get_analyzer() -> ProblemAnalyzer:
    return GeminiProblemAnalyzer.get_instance()


def get_problem(problem_id: int) -> models.Problem:
    try:
        return models.Problem.objects.get(pk=problem_id)
    except models.Problem.DoesNotExist:
        logger.warning(f'id가 {problem_id}인 문제를 찾을 수 없습니다.')


def get_problem_dto(problem: models.Problem) -> dto.ProblemDTO:
    return dto.ProblemDTO(
        title=problem.title,
        description=problem.description,
        input_description=problem.input_description,
        output_description=problem.output_description,
        memory_limit=problem.memory_limit,
        time_limit=problem.time_limit,
    )


def save_analysis(problem: models.Problem, analysis_dto: dto.ProblemAnalysisDTO) -> models.ProblemAnalysis:
    analysis = models.ProblemAnalysis(**{
        models.ProblemAnalysis.field_name.PROBLEM: problem,
        models.ProblemAnalysis.field_name.TIME_COMPLEXITY: analysis_dto.time_complexity,
        models.ProblemAnalysis.field_name.DIFFICULTY: enums.ProblemDifficulty.from_label(analysis_dto.difficulty),
        models.ProblemAnalysis.field_name.HINT: analysis_dto.hints,
    })
    analysis_tags = []
    for tag_key in analysis_dto.tags:
        try:
            tag = models.ProblemTag.objects.get(**{
                models.ProblemTag.field_name.KEY: tag_key,
            })
        except models.ProblemTag.DoesNotExist:
            logger.warn(f'문제 분석 결과에 알 수 없는 태그 [{tag_key}] 가 포함된 것을 발견하였습니다.')
            tag = models.ProblemTag.objects.create(**{
                models.ProblemTag.field_name.KEY: tag_key,
                models.ProblemTag.field_name.NAME_KO: f'존재하지 않는 태그: [{tag_key}]',
                models.ProblemTag.field_name.NAME_EN: f'존재하지 않는 태그: [{tag_key}]',
            })
        finally:
            analysis_tag = models.ProblemAnalysisTag(**{
                models.ProblemAnalysisTag.field_name.ANALYSIS: analysis,
                models.ProblemAnalysisTag.field_name.TAG: tag,
            })
            analysis_tags.append(analysis_tag)
    with atomic():
        analysis.save()
        models.ProblemAnalysisTag.objects.bulk_create(analysis_tags)
