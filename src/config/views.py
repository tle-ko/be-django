
from django.conf import settings
from django.views import debug


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
