# -*- coding: utf-8 -*-
from .celery import app as celery_app
import os
from app.config import settings


# add proxy
if settings.APP_USE_PROXY:
    os.environ['http_proxy'] = settings.APP_PROXY_SERVER
    os.environ['https_proxy'] = settings.APP_PROXY_SERVER
    if os.environ.get('no_proxy'):
        os.environ['no_proxy'] = settings.APP_NO_PROXY + ',' + os.environ.get('no_proxy')
    else:
        os.environ['no_proxy'] = settings.APP_NO_PROXY


# create logs dir
neccessary_dirs = (
    os.path.join(settings.APP_BASE_DIR, 'logs'),
    os.path.join(settings.APP_BASE_DIR, 'logs', 'celery'),
    os.path.join(settings.APP_BASE_DIR, 'logs', 'default'),
    os.path.join(settings.APP_BASE_DIR, 'logs', 'exceptions'),
    os.path.join(settings.APP_BASE_DIR, 'logs', 'uvicorn'),
    os.path.join(settings.APP_BASE_DIR, 'logs', 'gunicorn'),
)
for _dir in neccessary_dirs:
    if not os.path.isdir(_dir):
        os.makedirs(_dir)


__all__ = ('celery_app',)
