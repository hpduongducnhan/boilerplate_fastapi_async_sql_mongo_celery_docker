# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from typing import Dict, List
from celery import Celery
from app.config import settings


app = Celery('fastapi_app')


class CeleryTaskConfig:
    """     Redis       """
    my_redis = f"redis://:{settings.APP_REDIS_PASSWORD}@{settings.APP_REDIS_HOST}:{settings.APP_REDIS_PORT}/{settings.APP_REDIS_DB}"

    """     General settings        """
    accept_content = ['json']  # using serializer name
    result_accept_content = ['json']

    """     Time Setting        """
    enable_utc = False
    timezone = "Asia/Ho_Chi_Minh"

    """     Task setting        """
    result_backend = my_redis  # default: no result backend, to store task results
    task_ignore_result = False
    task_serializer = 'json'
    result_serializer = 'json'
    task_track_started = True

    task_queues = {
        'io_task': {},
        'cpu_task': {}
    }
    task_routes = {
        "io_*": {'queue': 'io_task'},
        "cpu_*": {'queue': 'cpu_task'},
        "*": {'queue': 'io_task'},
    }

    """     Broker      """
    broker_url = my_redis  # redis enough

    """     Worker       """
    # worker_state_db = '/opt/celery_services/state_db/worker_state.db'
    worker_concurrency = 4  # Default is number of cpu cores
    worker_prefetch_multiplier = 1  # disable prefetching -> each worker receive only 1 msg and process it, then receive
    worker_max_tasks_per_child = 1
    # task_time_limit = 1000

    """  Task Manager here, with this task manager, we can call any python file """
    # imports = ('tasks.poolip_find_duplicate', 'task_manager')
    # imports = ('task_manager',)

    # FOR CELERY BEAT $$$$$$$$$$$$$$$$$$$$$$$$$$$
    # beat_schedule_filename = "/var/run/celery/celerybeat-schedule"
    # beat_schedule_filename = os.getcwd()
    beat_max_loop_interval = 10
    beat_schedule = {}      # use schedule in database
    # beat_schedule = beat_schedule_register


app.config_from_object(CeleryTaskConfig)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks([
    'app.user',
    'app.notification',
    'app.telegram'
])


def send_task(task_name: str, task_args: List = [], task_kwargs: Dict = {}, **kwargs):
    return app.send_task(
        task_name, args=task_args, kwargs=task_kwargs,
        **kwargs
    )
