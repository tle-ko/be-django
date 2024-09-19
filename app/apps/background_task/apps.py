from datetime import timedelta
from logging import getLogger
from threading import Thread
from typing import TYPE_CHECKING

from django.apps import AppConfig
from django.conf import settings



if TYPE_CHECKING:
    from background_task.models import Task
else:
    Task = None


logger = getLogger(__name__)


class BackgroundTasksAppConfig(AppConfig):
    name = 'apps.background_task'
    from apps.background_task import __version__ as version_info
    verbose_name = 'Background Tasks ({})'.format(version_info)

    def ready(self):
        if settings.BACKGROUND_TASK_AUTO_RUN:
            logger.info('background tasks thread starting...')

            from apps.background_task import signals  # noqa
            from apps.background_task.management.commands.process_tasks import Command as ProcessTasksCommand

            def task_runner(*args, **kwargs):
                logger.info('background tasks thread started')
                try:
                    command = ProcessTasksCommand()
                    command.handle()
                except Exception as exception:
                    logger.error(exception)
                finally:
                    logger.info('shutting down background task thread.')

            thread = Thread(target=task_runner)
            thread.setDaemon(True)
            thread.start()
        else:
            logger.warning('background tasks thread disabled')


    def backoff(self, instance: Task) -> timedelta:
        return timedelta(seconds=60+instance.attempts)
