from tle.serializers.user_detail import UserDetailSerializer
from tle.serializers.user_minimal import UserMinimalSerializer
from tle.serializers.user_sign_in import UserSignInSerializer

from tle.serializers.problem_analysis import ProblemAnalysisSerializer
from tle.serializers.problem_detail import ProblemDetailSerializer
from tle.serializers.problem_difficulty import ProblemDifficultySerializer
from tle.serializers.problem_minimal import ProblemMinimalSerializer
from tle.serializers.problem_tag import ProblemTagSerializer

from tle.serializers.crew_member import CrewMemberSerializer


UserSerializer = UserDetailSerializer
ProblemSerializer = ProblemDetailSerializer


__all__ = (
    'UserSerializer',
    'UserDetailSerializer',
    'UserMinimalSerializer',
    'UserSignInSerializer',

    'ProblemSerializer',
    'ProblemAnalysisSerializer',
    'ProblemDetailSerializer',
    'ProblemDifficultySerializer',
    'ProblemMinimalSerializer',
    'ProblemTagSerializer',

    'CrewMemberSerializer',
)
