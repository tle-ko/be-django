"""이 서비스는 사용자 확인 절차를 수행하는 데 필요한 기능을 제공합니다.

사용자 확인 절차는 다음과 같습니다:
1. 사용자가 이메일 주소를 입력합니다.
2. 서버는 해당 이메일 주소로 인증 코드를 전송합니다.
3. 사용자는 인증 코드를 입력합니다.
4. 서버는 인증 코드를 확인합니다.
5. 서버는 인증 코드를 확인한 사용자에게 인증 토큰을 전송합니다.
6. 사용자는 회원가입 절차에서 인증 토큰을 입력합니다.
7. 서버는 인증 토큰을 확인하여 사용자를 확인합니다.
"""


class VerificationService:
    @staticmethod
    def is_verified(email: str) -> bool:
        pass

    @staticmethod
    def get_verification_code(email: str) -> str:
        pass

    @staticmethod
    def send_verification_code(email: str, verification_code: str) -> str:
        pass

    @staticmethod
    def get_verification_token(email: str, verification_code: str) -> str:
        pass

    @staticmethod
    def validate_verification_code(email: str, verification_code: str) -> None:
        pass

    @staticmethod
    def validate_verification_token(email: str, verification_token: str) -> None:
        pass
