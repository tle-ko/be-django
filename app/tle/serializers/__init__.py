from tle.serializers.problem_detail import ProblemDetailSerializer
from tle.serializers.problem_minimal import ProblemMinimalSerializer
from tle.serializers.problem_tag import ProblemTagSerializer

from tle.serializers.crew_detail import CrewDetailSerializer
from tle.serializers.crew_member import CrewMemberSerializer
from tle.serializers.crew_recruiting import CrewRecruitingSerializer
from tle.serializers.crew_joined import CrewJoinedSerializer


ProblemSerializer = ProblemDetailSerializer


__all__ = (
    'ProblemSerializer',
    'ProblemDetailSerializer',
    'ProblemMinimalSerializer',
    'ProblemTagSerializer',

    'CrewDetailSerializer',
    'CrewMemberSerializer',
    'CrewRecruitingSerializer',
    'CrewJoinedSerializer',
)
