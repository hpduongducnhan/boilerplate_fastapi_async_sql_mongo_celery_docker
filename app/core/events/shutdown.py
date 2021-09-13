# -*- coding: utf-8 -*-
from tortoise import Tortoise
from app.telegram.telegram_bot import send_message
from app.utils import strings


async def event_01_disconnect_database():
    await Tortoise.close_connections()


async def event_99_notify_app_stopped():
    await send_message('FastApi-Celery-App Stopped')


events = [v for k, v in locals().items() if k.startswith('event_')]
