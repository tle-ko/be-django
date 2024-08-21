import logging
from sys import stderr
from typing import Any

from django.conf import settings
from django.core.management.color import no_style
from django.utils.log import ServerFormatter
from django.views import debug


class ColorlessServerFormatter(ServerFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.style = no_style()


class FileAndStreamHandler(logging.FileHandler):
    """기본적으로 logging.FileHandler와 동일하나, STDERR에도 동일한 로그를 같이 출력해주는 Handler이다."""
    def emit(self, record: logging.LogRecord) -> None:
        self.stream, stream = stderr, self.stream
        super().emit(record)
        self.stream = stream
        super().emit(record)


class NACLExceptionReporter(debug.ExceptionReporter):
    def __init__(self, request, exc_type, exc_value, tb, is_email=False):
        self.logger = logging.getLogger('django.security.DisallowedHost')
        super().__init__(request, exc_type, exc_value, tb, is_email)

    def get_traceback_data(self) -> dict:
        """Return a dictionary containing traceback information."""
        if self._get_host() not in settings.ALLOWED_HOSTS:
            # IP, 혹은 AWS 도메인 주소 패턴을 이용하여 접속을 시도하는 악성 봇들에게
            # 환경변수나 기타 정보가 노출되지 않도록 함.
            self.logger.info(
                f'Illegal access detected from client "{self._get_client_ip_addr()}" to host "{self._get_host()}"'
            )
            return {}
        return super().get_traceback_data()

    def _get_host(self) -> str:
        return self.request._get_raw_host().split(':')[0]

    def _get_client_ip_addr(self) -> str:
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_addr = x_forwarded_for.split(',')[0]
        else:
            ip_addr = self.request.META.get('REMOTE_ADDR')
        return ip_addr
