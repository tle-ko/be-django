from typing import Any

from django.conf import settings
from django.core.management.color import no_style
from django.utils.log import ServerFormatter
from django.views import debug


class ColorlessServerFormatter(ServerFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.style = no_style()


class NACLExceptionReporter(debug.ExceptionReporter):
    def __init__(self, request, exc_type, exc_value, tb, is_email=False):
        super().__init__(request, exc_type, exc_value, tb, is_email)

    def get_traceback_data(self) -> dict:
        """Return a dictionary containing traceback information."""
        if self._get_domain() in settings.ALLOWED_HOSTS:
            return super().get_traceback_data()
        return {}

    def _get_domain(self):
        host = self.request._get_raw_host()
        return host.split(':')[0]
