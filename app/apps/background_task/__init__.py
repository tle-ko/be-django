# -*- coding: utf-8 -*-
__version__ = '1.2.8'

default_app_config = 'background_task.apps.BackgroundTasksAppConfig'

def background(*arg, **kw):
    from apps.background_task.tasks import tasks
    return tasks.background(*arg, **kw)
