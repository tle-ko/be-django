from logging import getLogger
from threading import Thread

from django.apps import AppConfig


logger = getLogger(__name__)


class BackgroundTasksAppConfig(AppConfig):
    name = 'apps.background_task'
    from apps.background_task import __version__ as version_info
    verbose_name = 'Background Tasks ({})'.format(version_info)

    def ready(self):
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
