from datetime import timedelta
import threading
import typing
from logging import getLogger

from django.apps import AppConfig
from django.conf import settings


if typing.TYPE_CHECKING:
    from background_task.models import Task
else:
    Task = None


logger = getLogger(__name__)


class BackgroundTasksAppConfig(AppConfig):
    name = 'apps.background_task'
    from apps.background_task import __version__ as version_info
    verbose_name = 'Background Tasks ({})'.format(version_info)

    def ready(self) -> None:
        from apps.background_task import signals  # noqa

        if settings.BACKGROUND_TASK_AUTO_RUN:
            logger.info('background task runner thread enabled.')
            self.run_background_tasks()
        else:
            logger.warning('background task runner thread disabled.')

    def run_background_tasks(self) -> None:
        from apps.background_task.management.commands.process_tasks import Command as ProcessTasksCommand

        def task_runner(*args, **kwargs):
            logger.info('task runner thread started.')
            try:
                command = ProcessTasksCommand()
                command.handle()
            except Exception as exception:
                logger.error(exception)
            finally:
                logger.info('task runner thread died.')

        thread = threading.Thread(target=task_runner)
        thread.setDaemon(True)
        thread.start()

    def backoff(self, instance: Task) -> timedelta:
        return timedelta(seconds=60+instance.attempts)
