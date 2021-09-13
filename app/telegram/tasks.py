# -*- coding: utf-8 -*-
from celery import shared_task
from app.utils import strings
from .telegram_bot import send_message
from datetime import datetime
from app.utils.asyncio_tools import celery_async_executor
from app.config import settings


@shared_task(name=strings.CTASK_NOTIFY_TELEGRAM_APP_STARTED)
def notify_telegram_when_app_started(msg: str = None):
    if not msg:
        msg = 'FastApi-Celery-App Started'
    celery_async_executor(
        send_message,
        f"{datetime.now()}\n{msg}"
    )
