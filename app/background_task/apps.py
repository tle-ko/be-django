from logging import getLogger
from threading import Thread

from django.apps import AppConfig


logger = getLogger(__name__)


class BackgroundTasksAppConfig(AppConfig):
    name = 'background_task'
    from background_task import __version__ as version_info
    verbose_name = 'Background Tasks ({})'.format(version_info)

    def ready(self):
        import background_task.signals  # noqa

        logger.info('creating thread for background tasks')

        from background_task.management.commands.process_tasks import Command as ProcessTasksCommand

        runner = ProcessTasksCommand()
        thread = Thread(target=runner.run)
        thread.setDaemon(True)
        thread.start()

        logger.info('background tasks thread started')
