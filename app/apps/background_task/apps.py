from datetime import timedelta
from typing import TYPE_CHECKING

from django.apps import AppConfig


if TYPE_CHECKING:
    from background_task.models import Task
else:
    Task = None


class BackgroundTasksAppConfig(AppConfig):
    name = 'apps.background_task'
    from apps.background_task import __version__ as version_info
    verbose_name = 'Background Tasks ({})'.format(version_info)

    def ready(self) -> None:
        from apps.background_task import signals  # noqa

    def backoff(self, instance: Task) -> timedelta:
        return timedelta(seconds=60+instance.attempts)
